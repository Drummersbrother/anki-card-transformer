import os
import glob
import genanki
import random


def gen_anki_decks():
    gen_guid = lambda: random.randrange(1 << 30, 1 << 31)
    apkg_basedir = "anki_packages"
    card_media_basedir = "card_media"

    mathjax_load_suffix = """
    <script type="text/x-mathjax-config">
    MathJax.Hub.processSectionDelay = 0;
    MathJax.Hub.Config({
      messageStyle: 'none',
      showProcessingMessages: false,
      tex2jax: {
        inlineMath: [['\\(', '\\)']],
        displayMath: [['\\[', '\\]']],
        processEscapes: true
      }
    });
    </script>
    <script type="text/javascript">
    (function() {
      if (window.MathJax != null) {
        var card = document.querySelector('.card');
        MathJax.Hub.Queue(['Typeset', MathJax.Hub, card]);
        return;
      }
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG';
      document.body.appendChild(script);
    })();
    </script>"""

    card_styling = """
    * { font-family: arial;
    font-size: 21px;
    text-align: left;
    color: black;
    background-color: #EEEEEE
    }
    img {
        height: auto;
        width: 50%;
    }"""

    template_head = """<head><meta charset="UTF-8"></head>"""

    # The idea is to create one deck for each topic, with tags indicating the original directory position
    # All notes are in HTML, but it should work, in the end...

    for topic_filename in glob.glob("parsed_cards/*"):
        topic_name = topic_filename.split('/')[-1]
        topic_deck = genanki.Deck(gen_guid(), topic_name)

        card_model = genanki.Model(
            gen_guid(),
            'IB Smart Prep model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': template_head + '<body> {{Question}} </body>' + mathjax_load_suffix,
                    'afmt': template_head + '<body> {{Answer}} </body>' + mathjax_load_suffix,
                },
            ],
            css=card_styling
        )

        topic_deck.add_model(card_model)

        # All the cards for this topic
        for parsed_card in glob.glob(f"parsed_cards/{topic_name}/**/*front.html", recursive=True):
            front_filename = parsed_card
            back_filename = parsed_card[:-10] + "back.html"

            # We read the front and back sides
            with open(front_filename, mode="r") as front_file:
                front_html = front_file.read()
            with open(back_filename, mode="r") as back_file:
                back_html = back_file.read()

            parsed_note = genanki.Note(
                model=card_model,
                fields=[front_html, back_html],
                sort_field=front_filename.split("/")[-1][:-11],
                tags=["ib_smart_prep_" + x for x in front_filename.split("/")[1:-1]]
            )

            topic_deck.add_note(parsed_note)

        print(topic_name, len(topic_deck.notes))

        # We add the media files to the deck, but due to genanki limitations, we have to enter the media directory first
        topic_package = genanki.Package(topic_deck)

        os.chdir(card_media_basedir)
        topic_package.media_files = glob.glob("*")

        topic_package.write_to_file("../" + apkg_basedir + "/" + topic_name + ".apkg")
        os.chdir("..")


if __name__ == "__main__":
    gen_anki_decks()
