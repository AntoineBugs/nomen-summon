import sys
import os

# Species
species_list = [
    "humain",
    "ange",
    "humain",
    "thérian",
    "humain",
    "robot",
    "humain",
    "dragon",
    "humain",
    "garou",
    "humain",
    "fée",
    "humain",
    "humain",
    "elfe",
    "humain",
    "vampire",
    "humain",
    "stellaire",
    "humain",
    "alien",
    "humain",
    "phytian",
    "humain",
    "démon",
    "humain",
]

filename = os.path.join(os.path.dirname(__file__), "species.txt")
with open(filename, "rt", encoding="utf8") as file:
    species_desc = file.readlines()
    for i, line in enumerate(species_desc):
        species_desc[i] = line.replace("\n", "")


species_zip = list(zip(species_list, species_desc))
species_dict = {index: t for index, t in enumerate(species_zip)}


# Items
item_classes = {
    "bmp": ("protection", 3, "objet"),
    "cklqx": ("source d'information", 5, "inclassable"),
    "dnt": ("arme", 8, "objet"),
    "fvw": ("vêtement", 3, "autre"),
    "gr": ("outil", 8, "objet"),
    "h": ("personnalisation", 1, "inclassable"),
    "jsz": ("familier", 5, "autre"),
}

composed_items = {
    "bmp+cklqx": ("guide de survie", 8, "objet"),
    "bmp+dnt": ("kit de combat", 11, "objet"),
    "bmp+fvw": ("armure", 6, "objet"),
    "bmp+gr": ("kit de survie", 11, "objet"),
    "bmp+h": ("talisman", 4, "objet"),
    "bmp+jsz": ("gardien", 8, "autre"),
    "cklqx+dnt": ("grimoire", 13, "objet"),
    "cklqx+fvw": ("smart textile", 8, "autre"),
    "cklqx+gr": ("objet connecté", 13, "objet"),
    "cklqx+h": ("mémo", 6, "autre"),
    "cklqx+jsz": ("assistant virtuel", 10, "autre"),
    "dnt+fvw": ("tenue de combat", 11, "autre"),
    "dnt+gr": ("matériel dangereux", 16, "objet"),
    "dnt+h": ("mod", 9, "objet"),
    "dnt+jsz": ("prédateur", 13, "autre"),
    "fvw+gr": ("uniforme", 11, "autre"),
    "fvw+h": ("retouche", 4, "autre"),
    "fvw+jsz": ("peluche", 8, "autre"),
    "gr+h": ("outil custom", 9, "objet"),
    "gr+jsz": ("animal de travail", 13, "autre"),
    "h+jsz": ("symbiote", 6, "autre"),
}


items_dict = {"simple": item_classes, "composed": composed_items}

vowels = "aeiouy"
list_vowels = list(vowels)
class_letters = list_vowels.copy()
for i, v in enumerate(list_vowels[:-1]):
    for w in list_vowels[i + 1 :]:
        class_letters.append(v + w)


# Classes
class_names = [
    "fanboy·girl",
    "geek",
    "nerd",
    "artiste",
    "militant",
    "mystique",
    "gamer",
    "critique",
    "fan-artiste",
    "cosplayer",
    "rôliste",
    "programmeur·se",
    "créateur·ice de contenu",
    "hacker",
    "transhumaniste",
    "vulgarisateur·ice",
    "bricoleur",
    "devin",
    "tatoueur·se",
    "enchanteur·resse",
    "sorcier·ère",
]

filename = os.path.join(os.path.dirname(__file__), "classes.txt")
with open(filename, "rt", encoding="utf8") as file:
    class_desc = file.readlines()
    for i, line in enumerate(class_desc):
        class_desc[i] = line.replace("\n", "")

class_zip = list(zip(class_letters, class_names, class_desc))
class_dict = {l: {"name": n, "desc": d} for (l, n, d) in class_zip}  # noqa: E741


# Powers
power_names = [
    "shifter",
    "empathe",
    "éveillé",
    "tulpamancien·ne",
    "chad",
    "quantique",
    "onironaute",
    "clairvoyant·e",
    "invocateur·rice",
    "protagoniste",
    "superposé·e",
    "guérisseur·se",
    "hypnotiseur·se",
    "leader",
    "auramancien·ne",
    "main verte",
    "dolittle",
    "radiesthésiste",
    "gourou",
    "médium",
    "oméga",
]

filename = os.path.join(os.path.dirname(__file__), "powers.txt")
with open(filename, "rt", encoding="utf8") as file:
    power_desc = file.readlines()
    for i, line in enumerate(power_desc):
        power_desc[i] = line.replace("\n", "")


power_letters = [letter + "n" for letter in class_letters]
power_zip = list(zip(power_letters, power_names, power_desc))
power_dict = {l: {"name": n, "desc": d} for (l, n, d) in power_zip}  # noqa: E741

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


gen_classes = {
    "a": "la fiction",
    "e": "le numérique",
    "i": "la connaissance",
    "o": "la création",
    "u": "l'activisme",
    "y": "l'ésotérisme",
}
