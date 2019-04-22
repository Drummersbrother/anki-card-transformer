import requests
import json
import os
import threading

def get_cards(cards_to_get, num_conc_downloads, auth_token):
    # Setup for getting data from smart-prep
    # The session in smart prep
    sp_cookies = {
    }
    sp_headers = {
        #"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Authorization": f"Bearer {auth_token}"

    }
    sp_sess = requests.Session()

    cards_gotten = set()
    flashcard_content_url = \
        lambda ix: \
        f"https://api.smart-prep.com/fca/student/flashcard/{ix}/content"

    flashcard_raws = {}
    flashcard_rawjson = {}

    Lock = threading.Lock
    gotten_lock = Lock()
    to_get_lock = Lock()
    flash_card_data_lock = Lock()
    print_lock = Lock()

    def get_card():
        while True:
            with to_get_lock:
                if len(cards_to_get) > 0:
                    inx = cards_to_get.pop()
                else:
                    return

            with gotten_lock:
                cards_gotten.add(inx)

            raw_data = requests.get(flashcard_content_url(inx), cookies=sp_cookies, headers=sp_headers).text
            json_data = json.loads(raw_data)
            with flash_card_data_lock:
                flashcard_raws[inx] = raw_data
                flashcard_rawjson[inx] = json_data

            referred_cards = set(json_data["siblingsData"]["nextTenSiblings"])
            referred_cards.update(set(json_data["siblingsData"]["prevTenSiblings"]))
            referred_cards.update(set(json_data["siblingsData"]["nextFiveSiblings"]))
            referred_cards.update(set(json_data["siblingsData"]["prevFiveSiblings"]))

            with print_lock:
                with gotten_lock:
                    referred_cards = referred_cards - cards_gotten
                    print("Gotten:", len(cards_gotten))

                with to_get_lock:
                    cards_to_get.update(referred_cards)
                    print("Get:", len(cards_to_get))

    download_threads = []
    for i in range(num_conc_downloads):
        t = threading.Thread(target=get_card)
        download_threads.append(t)
        t.start()
    for t in download_threads:
        t.join()

    # Storing downloaded cards to disk, with proper directory structure
    base_dir = os.getcwd() + "/cards"

    for card_id, card in flashcard_rawjson.items():
        card_directories = card["parentsData"]

        deepest_path = "/".join(x["title"].replace(" ", "_") for x in reversed(card_directories))
        full_dir_path = base_dir + "/" + deepest_path
        os.makedirs(full_dir_path, exist_ok=True)

        # We now have a folder, so we store the data
        with open(full_dir_path + "/" + str(card_id), mode="w+") as card_file:
            json.dump(flashcard_rawjson[card_id], card_file, indent=2, sort_keys=True)


if __name__ == "__main__":
    auth_token = "AUTH TOKEN HERE"

    # Setup for which places to suck cards from
    # We only need to have the beginning cards here, we will scrape
    cards_to_get = {
        10505,  # Che SL first card
        12388,  # Bio SL first card
        11291,  # Phy SL first card
        8965,  # Mat SL first card
        9654,  # Bio HL first card
        10070,  # Bio D SL first card
        10114,  # Bio D HL first card
        11092,  # Che D SL first card
        6077,  # Phy D SL first card
        12323,  # Mat SL first card
        11727,  # Eco SL first card
        12354,  # Mat HL first card
        12090,  # Eco HL first card
        #10209,  # Che HL first card
        11572,  # Phy HL first card
    }

    num_conc = 100

    get_cards(cards_to_get, num_conc, auth_token)

