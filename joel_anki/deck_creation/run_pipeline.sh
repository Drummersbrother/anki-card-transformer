#! /bin/bash
echo "Running pipeline to create anki deck from LAGA01 google doc!"
cd ~/progs/anki-card-transformer/joel_anki/deck_creation/
python3 get_docs_file.py
python3 extract_cards.py
python3 create_anki_deck.py

echo "Done creating anki deck from LAGA01 google doc!"