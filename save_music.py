import pretty_midi

# Define the sequence of generated notes
generated_notes = ['C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4', 'B6', 'C4', 'C4', 'C4']

# Create a PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI()

# Create an instrument instance (0 corresponds to Piano)
instrument = pretty_midi.Instrument(program=0)

# Define the duration for each note (in seconds)
note_duration = 0.5  # Change this value to increase or decrease note duration

# Initialize start time
start_time = 0

# Add notes to the instrument
for note_name in generated_notes:
    # Convert note name to MIDI note number
    note_number = pretty_midi.note_name_to_number(note_name)
    
    # Define end time for the note
    end_time = start_time + note_duration
    
    # Create a note object
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=end_time)
    
    # Append the note to the instrument
    instrument.notes.append(note)
    
    # Update start time for the next note
    start_time = end_time  # Set the start time for the next note

# Add the instrument to the MIDI data
midi_data.instruments.append(instrument)

# Save the MIDI file
midi_data.write('generated_music.mid')

print("MIDI file has been saved as 'generated_music.mid'.")
