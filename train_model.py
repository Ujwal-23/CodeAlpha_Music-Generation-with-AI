import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Dropout
from tensorflow.keras.utils import to_categorical
import pickle
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt

# Load notes from the pickle file
with open('data/notes.pkl', 'rb') as filepath:
    notes = pickle.load(filepath)

# Prepare sequences
sequence_length = 100

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
    network_output = to_categorical(network_output)  # Convert output to one-hot encoding

    return network_input, network_output, note_names

# Prepare the sequences for the model
network_input, network_output, note_names = prepare_sequences(notes, sequence_length)

# Define the model
num_notes = len(note_names)
model = Sequential()
model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=False))
model.add(Dropout(0.3))
model.add(Dense(num_notes))
model.add(Activation('softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Define callbacks for saving the model and early stopping
checkpoint = ModelCheckpoint('music_generation_model.keras', save_best_only=True, monitor='loss', mode='min')
early_stopping = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)

# Train the model with callbacks
epochs = 100  # You can adjust this
batch_size = 64  # You can adjust this

# Train the model and store the training history
history = model.fit(network_input, network_output, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint, early_stopping])

# Plot the training loss
plt.plot(history.history['loss'], label='Training Loss')
plt.title('Model Loss Over Epochs')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend()
plt.show()

# Save the trained model
model.save('music_generation_model.keras')
print("Model saved successfully!")
