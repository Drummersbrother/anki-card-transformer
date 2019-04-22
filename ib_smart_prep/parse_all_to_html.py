import json
import os
import glob

media_mapping = {}
images_to_get = []


def create_media_type_mapping():
    for media_filename in glob.glob("card_media/*"):
        media_file_split = media_filename[len("card_media/"):].split(".")
        media_mapping[int(media_file_split[0][9:])] = media_file_split[1]


def parse_node(obj_to_decode):
    tag_overrides = {
        "div":
            {
                "tr": "tr",
                "td": "td",
                "table smpp-table-3": "table",
            }
    }

    this_type = obj_to_decode["node"]
    if this_type == "text":
        return obj_to_decode["text"]
    elif this_type == "comment":
        return ""
    elif this_type == "element":
        tag_type = obj_to_decode["tag"]

        tag_attrs = obj_to_decode.get("attr", None)

        if tag_type in tag_overrides:
            if tag_attrs is not None and "class" in tag_attrs.keys():
                tag_class = tag_attrs["class"]
                if tag_class in tag_overrides[tag_type]:
                    tag_type = tag_overrides[tag_type][tag_class]

        if tag_type == "img" or tag_type == "object":
            images_to_get.append(tag_attrs["alt"])
            media_filetype = media_mapping.get(tag_attrs["alt"], "")
            if media_filetype != "":
                media_filetype = "." + media_filetype
            tag_attrs["src"] = f"card_img_{tag_attrs['alt']}{media_filetype}"
            tag_attrs["alt"] = f"card_img_{tag_attrs['alt']}{media_filetype}"
            if tag_type == "object":
                tag_type = "img"

        # TODO use these properly
        tag_dataattrs = obj_to_decode.get("dataAttributes", None)
        tag_id = obj_to_decode.get("id", None)
        tag_child = obj_to_decode.get("child", [])

        if tag_type == "formula":
            formula_raw = tag_child[0]["text"]
            mathjaxed_formula = f" \\[ {formula_raw} \\] "
            tag_child[0]["text"] = mathjaxed_formula

        # We convert all the data to proper strings to be concatenated, and create a proper opening tag
        open_tag_string = ""

        if tag_attrs is not None:
            if "style" in tag_attrs.keys():
                tag_attrs["style"] = " ".join(tag_attrs["style"])

        attrs_string = " ".join(
            key + "=" + f"\"{val}\""
            for key, val in tag_attrs.items()
        ) if tag_attrs is not None else ""

        id_string = f"id=\"{tag_id}\"" if tag_id is not None else ""

        open_tag_string += f"<{tag_type} {id_string} {attrs_string}>"

        # See https://blog.teamtreehouse.com/to-close-or-not-to-close-tags-in-html5
        no_closing_tags = {"img", "input", "br", "hr", "meta"}
        closing_tag_string = f"</{tag_type}>" if tag_type not in no_closing_tags else ""

        if len(tag_child) > 0:
            return open_tag_string + decode_html(tag_child) + closing_tag_string
        else:
            return open_tag_string + closing_tag_string


def decode_html(to_parse):
    if type(to_parse) == str:
        obj_to_decode = json.loads(to_parse)
    else:
        obj_to_decode = to_parse

    total_string = ""
    for node in obj_to_decode:
        total_string += parse_node(node)

    return total_string


def encapsulate_html(to_encapsulate):
    html_head = ""
    html_body_prefix = ""
    html_body_suffix = ""

    total_string = html_head + html_body_prefix
    total_string += decode_html(to_encapsulate)
    total_string += html_body_suffix
    return total_string


def parse_cards():

    card_basedir = "cards"
    parsed_card_basedir = "parsed_cards"

    # Make sure we can handle media files properly
    create_media_type_mapping()

    # Loop through all the card to convert them
    for card_fname in glob.glob(card_basedir + "/**/*", recursive=True):
        card_loc = card_fname.split("/")
        if not card_loc[-1].isdigit():
            continue
        parsed_card_loc = card_loc.copy()
        parsed_card_loc[0] = parsed_card_basedir

        # We read and parse the card
        with open("/".join(card_loc), mode="r") as card_file:
            card_data = json.load(card_file)

        card_content_unparsed = card_data["content"]
        card_front_unparsed = card_content_unparsed[0]["content"]
        # Some cards don't have an answer side, and will thus be ignored
        if len(card_content_unparsed) < 2:
            continue
        card_back_unparsed = card_content_unparsed[1]["content"]

        card_front_html = encapsulate_html(card_front_unparsed)
        card_back_html = encapsulate_html(card_back_unparsed)

        # We save the html to disk
        os.makedirs("/".join(parsed_card_loc[:-1]), exist_ok=True)
        with open("/".join(parsed_card_loc)+".front.html", "w+") as parsed_card_file:
            parsed_card_file.write(card_front_html)
        with open("/".join(parsed_card_loc)+".back.html", "w+") as parsed_card_file:
            parsed_card_file.write(card_back_html)

    return set(images_to_get)


if __name__ == "__main__":
    print(parse_cards())

