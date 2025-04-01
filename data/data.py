import sys
import json
import os

VARIANT = "heroic_fantasy"

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, "variants", VARIANT)

# Species
filename = os.path.join(dirname, "species.json")
with open(filename, "r", encoding='utf-8') as f:
    species_dict = json.load(f, )
species_dict = {int(k): v for k, v in species_dict.items()}

# Items
filename = os.path.join(dirname, "items.json")
with open(filename, "r", encoding='utf-8') as f:
    items_dict = json.load(f, parse_int=int)

vowels = "aeiouy"
list_vowels = list(vowels)
class_letters = list_vowels.copy()
for i, v in enumerate(list_vowels[:-1]):
    for w in list_vowels[i + 1 :]:
        class_letters.append(v + w)


# Classes
filename = os.path.join(dirname, "classes.json")
with open(filename, "r", encoding='utf-8') as f:
    class_dict = json.load(f)

# Powers
filename = os.path.join(dirname, "powers.json")
with open(filename, "r", encoding='utf-8') as f:
    power_dict = json.load(f)

aptitudes = {"classes": class_dict, "powers": power_dict}

# Mastery levels
import bisect

apt_mastery = [
    (0, 50, "base"),
    (50, 100, "avancé"),
    (100, 200, "maître"),
    (200, sys.maxsize, "élite"),
]


def find_mastery_lvl(lvl):
    """
    Determines the mastery level based on the given level.

    Args:
        lvl (int): The level to find the corresponding mastery for.

    Returns:
        str: The mastery level corresponding to the given level. Returns an empty string if no mastery level is found.
    """
    mastery = ""
    idx = bisect.bisect_right([x[0] for x in apt_mastery], lvl)
    if idx > 0:
        mastery = apt_mastery[idx - 1][2]
    return mastery

filename = os.path.join(dirname, "gen_classes.json")
with open(filename, "r", encoding='utf-8') as f:
    gen_classes = json.load(f)
