import sys
import os

# Species
species_list = [
    "loup-garou",
    "ange",
    "orc",
    "harpie",
    "dragonide",
    "gobelin",
    "nain",
    "faune",
    "elfe",
    "félice",
    "vampire",
    "reptilien",
    "géant",
    "humain",
    "démon",
    "naga",
    "fée",
    "féloure",
    "selkie",
    "gnome",
    "centaure",
    "troll",
    "kelpie",
    "sirène",
    "golem",
    "minotaure",
]

filename = os.path.abspath("species.txt")
with open(filename, "rt", encoding="utf8") as file:
    species_desc = file.readlines()
    for i, line in enumerate(species_desc):
        species_desc[i] = line.replace("\n", "")


species_zip = list(zip(species_list, species_desc))
species_dict = {index: t for index, t in enumerate(species_zip)}


# Items
item_classes = {
    "bmp": ("armure/bouclier", 3, "objet"),
    "gr": ("altération physique", 8, "inclassable"),
    "dnt": ("arme/outil", 8, "objet"),
    "fvw": ("personnalisation", 0, "autre"),
    "h": ("vêtement/accessoire", 1, "objet"),
    "cklqx": ("source de pouvoir", 10, "inclassable"),
    "jsz": ("familier", 5, "autre"),
}

composed_items = {
    "bmp+gr": ("prothèse défensive", 11, "objet"),
    "bmp+dnt": ("armure équipée", 11, "objet"),
    "bmp+fvw": ("armure familiale", 3, "objet"),
    "bmp+h": ("amulette", 4, "objet"),
    "bmp+cklqx": ("armure de puissance", 13, "objet"),
    "bmp+jsz": ("armure vivante", 8, "autre"),
    "gr+dnt": ("prothèse offensive", 16, "objet"),
    "gr+fvw": ("membre/organe supplémentaire", 8, "autre"),
    "gr+h": ("augmentation physique", 9, "autre"),
    "gr+cklqx": ("relique", 18, "autre"),
    "gr+jsz": ("symbiote", 13, "autre"),
    "dnt+fvw": ("arme familiale", 8, "objet"),
    "dnt+h": ("belle arme", 9, "objet"),
    "dnt+cklqx": ("arme stimulante", 18, "objet"),
    "dnt+jsz": ("arme vivante", 13, "autre"),
    "fvw+h": ("tenue d'apparât", 1, "objet"),
    "fvw+cklqx": ("entraînement particulier", 10, "inclassable"),
    "fvw+jsz": ("esprit protecteur", 5, "autre"),
    "h+cklqx": ("tenue de combat", 11, "objet"),
    "h+jsz": ("monture", 6, "autre"),
    "cklqx+jsz": ("gardien de trésor", 15, "autre"),
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
    "mage",
    "archer",
    "bretteur",
    "lutteur",
    "acrobate",
    "technicien",
    "aéronaute",
    "paladin",
    "berserker",
    "barde",
    "alchimiste",
    "chevalier",
    "chasseur",
    "éclaireur",
    "pistolier",
    "gladiateur",
    "assassin",
    "forgeron",
    "danseur",
    "soigneur",
    "voleur",
]

filename = os.path.abspath(
    os.path.join("data", "variants", "urban_fantasy", "classes.txt")
)
with open(filename, "rt", encoding="utf8") as file:
    class_desc = file.readlines()
    for i, line in enumerate(class_desc):
        class_desc[i] = line.replace("\n", "")

class_zip = list(zip(class_letters, class_names, class_desc))
class_dict = {l: {"name": n, "desc": d} for (l, n, d) in class_zip}  # noqa: E741


# Powers
power_names = [
    "arcaniste",
    "élémentaliste",
    "chaman",
    "métamorphe",
    "téléporteur",
    "télépathe",
    "évocateur",
    "pactisant",
    "nécromancien",
    "marche-temps",
    "marionnettiste",
    "enchanteur",
    "druide",
    "météomage",
    "faiseur de golems",
    "avatar",
    "invocateur",
    "marabout",
    "métromage",
    "doppelganger",
    "onironaute",
]

filename = os.path.abspath("powers.txt")
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


gen_classes = {
    "a": "la magie",
    "e": "l'archerie",
    "i": "l'escrime",
    "o": "la lutte",
    "u": "l'acrobatie",
    "y": "la science",
}
