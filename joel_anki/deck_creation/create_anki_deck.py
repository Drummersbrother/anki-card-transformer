import genanki
import json
import os

with open(os.path.join("second_pass", "card_groupings.json"), mode="r") as groupings_file:
    card_groupings = json.load(groupings_file)

# Very magic number
guid = 42069
apkg_basedir = "outputs"

card_styling = """
    .card { 
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
    }
    img {
        height: auto;
        width: 50%;
    }"""

template_head = """<head><meta charset="UTF-8"></head>"""

# The idea is to create one deck for each keybinding, with tags indicating the original directory position
# All notes are in HTML, but it should work, in the end...

jur_deck = genanki.Deck(guid, "LAGA01 - Från docs")

card_model = genanki.Model(
    guid,
    'LAGA01 Model, auto',
    fields=[
        {'name': 'Koncept'},
        {'name': 'Beskrivning'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': template_head + '<body> {{Koncept}} </body>',
            'afmt': template_head + '<body> {{FrontSide}} <hr id=answer> {{Beskrivning}} </body>',
        },
    ],
    css=card_styling
)

jur_deck.add_model(card_model)

# Create the cards
for group in card_groupings:
    prompt = group[0]
    prompt = prompt.strip().strip(":")
    answer = group[1:]
    answer_text = " <br> ".join(answer)

    note = genanki.Note(
        model=card_model,
        fields=[prompt, answer_text],
        sort_field=prompt,
        tags=["laga01-docs-autokort"]
    )

    jur_deck.add_note(note)

    print("Added anki note:")
    print("Prompt:")
    print("\t" + prompt)
    print("Answer:")
    print("\t" + answer_text)

jur_package = genanki.Package(jur_deck)
jur_package.write_to_file(os.path.join(apkg_basedir, "jur_docs_autodeck.apkg"))
