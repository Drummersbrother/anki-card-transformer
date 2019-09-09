import falcon
import subprocess
import os
import io

pipeline_script_path = os.path.join("deck_creation", "run_pipeline.sh")
anki_deck_path = os.path.join("deck_creation", "outputs", "jur_docs_autodeck.apkg")

class GetAnkideck:
    def on_get(self, req, resp):
        """Gives back an anki .apkg file"""

        # Create the deck
        subprocess.call(pipeline_script_path)

        resp.status = falcon.HTTP_200
        resp.content_type = "application/octet-stream"
        resp.stream, resp.content_length = io.open(anki_deck_path), os.path.getsize(anki_deck_path)
        resp.downloadable_as = "jur_docs.apkg"

app = falcon.API()
app.add_route('/getdeck', GetAnkideck())