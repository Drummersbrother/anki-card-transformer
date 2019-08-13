from music21 import *

scale_streams = []
scale_types = [
    scale.MajorScale,
    scale.DorianScale,
    scale.PhrygianScale,
    scale.LydianScale,
    scale.MixolydianScale,
    scale.MinorScale,
    scale.LocrianScale
]

scale_name_to_swe = {
    "major": "Dur / Jonisk",
    "dorian": "Dorisk",
    "phrygian": "Frygisk",
    "lydian": "Lydisk",
    "mixolydian": "Mixolydisk",
    "minor": "Ren moll / Eolisk",
    "locrian": "Lokrisk",
}

origin_tones = [str(tone) for tone in [pitch.Pitch("E2").transpose(i) for i in range(12)]]
for origin_tone in origin_tones:
    scale_score = stream.Score()
    scale_stream = stream.Stream()
    scale_stream.clef = clef.BassClef()
    scale_stream.append(meter.TimeSignature("4/4"))

    for inx, scale_type in enumerate(scale_types):
        gen_scale = scale_type(tonic=origin_tone)
        origin_pitch = pitch.Pitch(gen_scale.getTonic())
        octaved_pitch = origin_pitch.transpose(12)
        scale_m = stream.Measure()

        if inx == 0:
            scale_te = expressions.TextExpression(origin_tone[:-1].capitalize())
            scale_te.positionPlacement = "above"
            scale_te.style.fontSize = 20.0
            scale_m.append(scale_te)

        modus_te = expressions.TextExpression(scale_name_to_swe[str(gen_scale.type)])
        modus_te.style.fontSize = 12.0
        modus_te.style.letterSpacing = 0.8
        scale_m.append(modus_te)

        for tone in gen_scale.getPitches(origin_pitch, octaved_pitch):
            scale_note = note.Note(tone, type="eighth")
            scale_m.append(scale_note)

        scale_m.rightBarline = bar.Barline("double")

        scale_stream.append(scale_m)


    scale_m.rightBarline = bar.Barline("final")
    scale_score.insert(0, metadata.Metadata())
    scale_score.metadata.title = f"Modala {origin_tone[:-1]}-skalor"
    scale_score.metadata.composer = 'Hugo Berg'
    scale_score.append(scale_stream)
    scale_streams.append(scale_score)

for scale_stream in scale_streams:
    scale_stream.write(fmt="musicxml", fp="outputs/" + scale_stream[0].title.replace(" ", "_") + ".xml")
