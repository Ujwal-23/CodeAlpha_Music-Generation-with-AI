import numpy as np
from keras.models import load_model
import pickle

# Load the trained model
model = load_model('music_generation_model.keras')

# Load notes from the pickle file
with open('data/notes.pkl', 'rb') as filepath:
    notes = pickle.load(filepath)

# Prepare the note-to-int and int-to-note mappings
note_names = sorted(set(notes))  # Get unique notes
valid_notes = [note for note in note_names if note not in ['7.10.2', '9.2', '10.2', '7.10', '10', '5.9']]  # Exclude known invalid notes
note_to_int = {note: num for num, note in enumerate(valid_notes)}
index_to_note = {num: note for num, note in enumerate(valid_notes)}

# Function to generate music
def generate_music(model, start_sequence, num_generate=100, temperature=1.0):
    generated_music = []
    sequence = start_sequence

    for _ in range(num_generate):
        prediction_input = np.reshape(sequence, (1, len(sequence), 1))  # Reshape for LSTM input
        prediction = model.predict(prediction_input, verbose=0)

        # Apply temperature scaling
        prediction = np.asarray(prediction).astype(float) ** (1 / temperature)
        prediction /= np.sum(prediction)  # Normalize to get probabilities

        # Select a valid note index based on the predicted probabilities
        index = np.random.choice(range(len(prediction[0])), p=prediction[0])
        
        # Check if the index corresponds to a valid note
        if index in index_to_note:
            generated_music.append(index)
            sequence = np.append(sequence, index)[1:]  # Update the sequence
        else:
            # If the index is invalid, repeat the process
            while index not in index_to_note:
                index = np.random.choice(range(len(prediction[0])), p=prediction[0])
            generated_music.append(index)
            sequence = np.append(sequence, index)[1:]  # Update the sequence

    return generated_music

def filter_repetitions(generated_notes, max_repeats=3):
    filtered_notes = []
    count = 1
    
    for i in range(len(generated_notes)):
        if i == 0 or generated_notes[i] != generated_notes[i - 1]:
            count = 1
            filtered_notes.append(generated_notes[i])
        elif count < max_repeats:
            filtered_notes.append(generated_notes[i])
            count += 1

    return filtered_notes

if __name__ == "__main__":
    # Use the first sequence from your training input as the start sequence
    sequence_length = 100  # Define your sequence length
    start_sequence = np.array([note_to_int[note] for note in notes[:sequence_length] if note in note_to_int]).flatten()

    generated_indices = generate_music(model, start_sequence, num_generate=100, temperature=0.8)  # Adjust temperature as needed

    # Convert generated indices to notes
    generated_notes = [index_to_note.get(index, None) for index in generated_indices]

    # Filter out None values (which correspond to invalid indices)
    generated_notes = [note for note in generated_notes if note is not None]

    # Apply post-processing to remove excessive repetitions
    generated_notes = filter_repetitions(generated_notes)

    print("Filtered generated music sequence in notes:", generated_notes)
