#! /usr//bin/python3
import os
import glob
import genanki
import random


def gen_anki_decks():
    gen_guid = lambda: random.randrange(1 << 30, 1 << 31)
    apkg_basedir = "anki_packages"

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

    keybinding_deck = genanki.Deck(gen_guid(), "Vim Keybindings, autogen")

    card_model = genanki.Model(
        gen_guid(),
        'Vim Keybinding Autogen Model',
        fields=[
            {'name': 'Keybinding'},
            {'name': 'Description'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': template_head + '<body> <tt> {{Keybinding}} </tt> </body>',
                'afmt': template_head + '<body> {{FrontSide}} <hr id=answer> {{Description}} </body>',
            },
        ],
        css=card_styling
    )

    keybinding_deck.add_model(card_model)

    # All the cards for this keybinding
    for parsed_card in glob.glob("parsed_keybindings/*"):
        keybinding_key = parsed_card.split("/")[-1]

        # We read the front and back sides
        with open(parsed_card, mode="r") as front_file:
            keybinding_description = front_file.read()
        # Because we can't have / in regular filenames
        keybinding_key = keybinding_key.replace("BACKSLASH", "/")

        parsed_note = genanki.Note(
            model=card_model,
            fields=[keybinding_key, keybinding_description],
            sort_field=keybinding_key,
            tags=["vim-keybinding-autogen"]
        )

        keybinding_deck.add_note(parsed_note)

    keybinding_package = genanki.Package(keybinding_deck)

    keybinding_package.write_to_file(apkg_basedir + "/" + "vim_keybinding_autogen" + ".apkg")

if __name__ == "__main__":
    gen_anki_decks()
