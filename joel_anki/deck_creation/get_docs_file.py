import json
import requests

print("Downloading the docs file!")

with open("config.json", mode="r") as config_file:
    config = json.load(config_file)

gdoc_raw_url = config["google_doc_link"]
gdoc_file_id = gdoc_raw_url[len("https://docs.google.com/document/d/"):]
gdoc_file_id = gdoc_file_id[:gdoc_file_id.find("/")]

gdoc_get_url = f"https://docs.google.com/document/d/{gdoc_file_id}/export?format=txt"
r = requests.get(gdoc_get_url)
chunk_size = 50 * 2**10
with open("first_pass/raw_text.txt", "wb") as fd:
    fd.write(r.content)

print("Done downloading the docs file!")

