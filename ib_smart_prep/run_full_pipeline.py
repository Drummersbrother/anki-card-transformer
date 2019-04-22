import get_all_cards, get_all_media_files, parse_all_to_html, parse_html_to_anki, parameters
import time
import os

"""This script takes a list of card ids and downloads + processes and sorts the full courses from those ids."""

# If the folders don't exist, we create them, as well as entering the data directory
data_folder = "data"
folders = ["anki_packages",
           "card_media",
           "cards",
           "parsed_cards"]
os.makedirs("data", exist_ok=True)
os.chdir("data/")
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# The cards from which we get the rest of them
beginning_cards = {
    12388, # Bio SL first card
    9654,  # Bio HL first card
    9855,  # Bio A SL first card
    9895,  # Bio A HL first card
    9928,  # Bio B SL first card
    9969,  # Bio B HL first card
    9996,  # Bio C SL first card
    10046, # Bio C HL first card
    10070, # Bio D SL first card
    10114, # Bio D HL first card
    10505, # Che SL first card
    10209, # Che HL first card
    10437, # Che A SL first card
    10030, # Che A HL first card
    10873, # Che B SL first card
    10930, # Che B HL first card
    10982, # Che C SL first card
    11038, # Che C HL first card
    11092, # Che D SL first card
    11143, # Che D HL first card
    11290, # Phy SL first card
    11572, # Phy HL first card
    5813,  # Phy A SL first card
    5856,  # Phy A HL first card
    5887,  # Phy B SL first card
    5933,  # Phy B HL first card
    5973,  # Phy C SL first card
    6041,  # Phy C HL first card
    6077,  # Phy D SL first card
    6136,  # Phy D HL first card
    12323, # Mat SL first card
    12354, # Mat HL first card
    9407,  # Mat Studies SL first card
    11726, # Eco SL first card
    12090, # Eco HL first card
    4596,  # ES&S first card
}

# The auth token for our session
auth_token = parameters.auth_token

# How many concurrent downloads to allow
num_conc_downloads = 100

start_time = time.time()

# We download the raw card data
get_all_cards.get_cards(beginning_cards, num_conc_downloads, auth_token)

# We parse for media references
media_files_to_get = parse_all_to_html.parse_cards()

# We download the media
get_all_media_files.get_media_files(media_files_to_get, num_conc_downloads, auth_token)

# We parse the cards to html with proper media references
parse_all_to_html.parse_cards()

# We parse the html into anki decks
parse_html_to_anki.gen_anki_decks()

# Done!
print(f"\nDone! The whole process took {round(time.time() - start_time, 2)} seconds.")
