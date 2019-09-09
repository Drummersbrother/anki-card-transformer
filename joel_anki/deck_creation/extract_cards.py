import re
import os
import json
from docx import Document

with open(os.path.join("first_pass", "raw_text.txt"), "r", encoding="utf-8") as f:
    doc = f.read()

raw_lines = doc.split("\n")

grouping_matcher = re.compile(r"(^\*\s[1-9][0-9]*\.)|(:)")

card_groupings = []
group = []
for inx, line in enumerate(raw_lines):
    if line == "":
        if len(group) != 0:
            card_groupings.append(group)
            #print("Created card group:")
            #print("  " + "\n\t".join(group))
            group = []
    elif len(group) != 0 and not grouping_matcher.findall(line):
        group.append(line[2:])
    elif grouping_matcher.findall(line):
        group.append(line[2:])

card_groupings = [([group[0][:group[0].find(":")], group[0][group[0].find(":")+2:]] if len(group) == 1 else group)
                  for group in card_groupings]

with open(os.path.join("second_pass", "card_groupings.json"), mode="w+") as output_file:
    json.dump(card_groupings, output_file)
