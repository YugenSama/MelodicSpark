import os
from mingus.core import scales
from mingus.containers import NoteContainer, Track, Composition
from mingus.midi import midi_file_out

def analyze_input(user_input):
    if isinstance(user_input, str):
        char_codes = [ord(c) for c in user_input if c.strip()]
        return {'type': 'text', 'values': char_codes}
    elif isinstance(user_input, (list, tuple)):
        return {'type': 'numbers', 'values': user_input}
    else:
        raise ValueError("Input must be a string or a list of numbers")

def generate_musical_elements(analysis):
    values = analysis['values']
    root_note = ['C', 'D', 'E', 'F', 'G', 'A', 'B'][sum(values) % 7]
    scale_type = ['major', 'minor', 'harmonic_minor', 'dorian', 'mixolydian'][len(values) % 5]

    scale_map = {
        'major': scales.Major,
        'minor': scales.NaturalMinor,
        'harmonic_minor': scales.HarmonicMinor,
        'dorian': scales.Dorian,
        'mixolydian': scales.Mixolydian
    }

    scale = scale_map[scale_type](root_note).ascending()

    melody_notes = []
    for v in values:
        note_name = scale[v % len(scale)]
        octave = 4 + (v % 3)
        melody_notes.append(f"{note_name}-{octave}")
    
    chord_progression = []
    for i in range(min(len(values), 8)):
        base = values[i] % len(scale)
        chord = [scale[(base + j) % len(scale)] for j in [0, 2, 4]]
        chord_progression.append(chord)

    return {
        'melody': melody_notes,
        'chord_progression': chord_progression
    }

def create_composition(musical_elements):
    comp = Composition()
    track = Track()
    for chord in musical_elements['chord_progression']:
        nc = NoteContainer(chord)
        track.add_notes(nc, 4)
    for note_str in musical_elements['melody']:
        track.add_notes(note_str, 2)
    comp.add_track(track)
    return comp

def save_to_midi(comp, filename):
    midi_file_out.write_Composition(filename, comp)

def generate_music(user_input):
    analysis = analyze_input(user_input)
    elements = generate_musical_elements(analysis)
    return create_composition(elements)

if __name__ == "__main__":
    user_input = input("Enter a sentence or a list of numbers (e.g. Hello or 1,2,3): ")

    if ',' in user_input:
        try:
            user_input_numbers = [int(num.strip()) for num in user_input.split(',')]
            composition = generate_music(user_input_numbers)
        except ValueError:
            print("Invalid number format.")
            exit()
    elif user_input.strip():
        composition = generate_music(user_input.strip())
    else:
        print("No input received.")
        exit()

    output_path = input("Enter output MIDI file path (e.g. my_music.mid): ").strip()
    if not output_path.endswith(".mid"):
        output_path += ".mid"

    save_to_midi(composition, output_path)
    print(f"MIDI file created: {output_path}")
