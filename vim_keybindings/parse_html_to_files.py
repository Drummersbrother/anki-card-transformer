#! /usr/bin/python3
import bs4

raw_html_filename = "raw_keybinding_page.html"
keybinding_dirname = "parsed_keybindings"

with open(raw_html_filename, mode="r") as raw_html_file:
    raw_html = raw_html_file.read()

bs = bs4.BeautifulSoup(raw_html, features="lxml")

lis = bs.findAll("li")
split_lis = [str(li) for li in lis]
split_lis = [li.strip().split("<!-- -->") for li in split_lis]
from pprint import pprint
split_lis = [["".join(entry[:-1]), entry[-1]] for entry in split_lis]

split_lis = [[li[0][len("<li>"):-len(" - ")], li[1][:-len("</li>")]] for li in split_lis]
split_lis = [[bs4.BeautifulSoup(pli).get_text() for pli in li] for li in split_lis]
split_lis = [[li[0], li[1].capitalize()] for li in split_lis]
remappings = {".": " . "}
for keybinding, description in split_lis:
    keybinding = keybinding.replace("/", "BACKSLASH")
    if keybinding in remappings.keys():
        keybinding = remappings[keybinding]
    with open(keybinding_dirname + "/" + keybinding, mode="w+") as keybinding_file:
        keybinding_file.write(description)
    print("Wrote to file:", keybinding)

