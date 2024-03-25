import sys

# Species
species_list = [
    "ange",
    "thérian",
    "robot",
    "dragon",
    "garou",
    "fée",
    "humain",
    "elfe",
    "vampire",
    "stellaire",
    "alien",
    "phytian",
    "démon",
]

filename = "species.txt"
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
    "gr": ("outil", 8, "inclassable"),
    "h": ("personnalisation", 1, "objet"),
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
    "cklqx+fvw": ("smart textile", 8, "inclassable"),
    "cklqx+gr": ("objet connecté", 13, "autre"),
    "cklqx+h": ("mémo", 6, "objet"),
    "cklqx+jsz": ("assistant virtuel", 10, "autre"),
    "dnt+fvw": ("tenue de combat", 11, "objet"),
    "dnt+gr": ("matériel dangereux", 16, "objet"),
    "dnt+h": ("mod", 9, "objet"),
    "dnt+jsz": ("prédateur", 13, "autre"),
    "fvw+gr": ("uniforme", 11, "autre"),
    "fvw+h": ("retouche", 4, "objet"),
    "fvw+jsz": ("peluche", 8, "autre"),
    "gr+h": ("outil custom", 9, "autre"),
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

filename = "classes.txt"
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

filename = "powers.txt"
with open(filename, "rt", encoding="utf8") as file:
    power_desc = file.readlines()
    for i, line in enumerate(power_desc):
        power_desc[i] = line.replace("\n", "")


power_letters = [letter + "n" for letter in class_letters]
power_zip = list(zip(power_letters, power_names, power_desc))
power_dict = {l: {"name": n, "desc": d} for (l, n, d) in power_zip}  # noqa: E741

aptitudes = {"classes": class_dict, "powers": power_dict}

# Mastery levels
apt_mastery = {
    "base": range(50),
    "avancé": range(50, 100),
    "maître": range(100, 200),
    "élite": range(200, sys.maxsize),
}


def find_mastery_lvl(lvl):
    mastery = ""
    for k, v in apt_mastery.items():
        if lvl in v:
            mastery = k
            break
    return mastery
