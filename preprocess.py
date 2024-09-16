import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
from tensorflow.keras.utils import to_categorical  # Import for one-hot encoding

def get_notes():
    """ Extracts notes and chords from the MIDI files and saves them as a list """
    notes = []

    for file in glob.glob("data/*.mid"):
        midi = converter.parse(file)

        # Try to partition by instrument
        parts = instrument.partitionByInstrument(midi)
        if parts:
            for part in parts.parts:
                if 'Piano' in str(part):
                    for element in part.recurse():
                        if isinstance(element, note.Note):
                            notes.append(str(element.pitch))
                        elif isinstance(element, chord.Chord):
                            notes.append('.'.join(str(n) for n in element.normalOrder))
        else:
            for element in midi.flat.notes:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    # Debug print to check the number of notes extracted
    print(f"Extracted {len(notes)} notes from MIDI files.")
    
    # Save the notes to a file
    with open('data/notes.pkl', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

def prepare_sequences(notes, sequence_length):
    """ Prepare the sequences used by the Neural Network """
    # 1. Map notes to integers
    note_names = sorted(set(notes))  # Get all unique notes
    note_to_int = {note: num for num, note in enumerate(note_names)}  # Assign unique integers to notes

    # 2. Prepare input-output sequences
    network_input = []
    network_output = []

    # Create sequences of notes and corresponding outputs
    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]  # Input sequence (e.g., 100 notes)
        sequence_out = notes[i + sequence_length]  # Next note (the output)
        network_input.append([note_to_int[char] for char in sequence_in])  # Convert input sequence to integers
        network_output.append(note_to_int[sequence_out])  # Convert output note to integer

    # 3. Reshape the input for the LSTM
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))  # Shape: (samples, time steps, features)

    # 4. Normalize the input
    network_input = network_input / float(len(note_names))  # Normalize to range [0, 1]

    # 5. One-hot encode the output
    if network_output:  # Check if network_output is not empty
        network_output = to_categorical(network_output)  # Convert output to one-hot encoding
    else:
        print("Warning: network_output is empty. No sequences were created.")
        return None, None, note_names  # Handle this case appropriately

    return network_input, network_output, note_names

if __name__ == "__main__":
    notes = get_notes()
    
    # Check if notes are extracted
    if not notes:
        print("No notes extracted. Exiting.")
        exit()  # Exit if no notes are found

    sequence_length = 100  # Set the sequence length (number of notes in each sequence)
    network_input, network_output, note_names = prepare_sequences(notes, sequence_length)

    if network_input is not None and network_output is not None:
        print(f"Prepared {len(network_input)} sequences for training.")
    else:
        print("No valid input-output sequences prepared.")
