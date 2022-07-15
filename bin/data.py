import pickle
import os


# Species
species_list = ["loup-garou", "ange", "orc", "harpie", "dragonide", "gobelin", "nain",
                "faune", "elfe", "félice", "vampire", "reptilien", "géant", "humain",
                "démon", "naga", "fée", "féloure", "selkie", "gnome", "centaure",
                "troll", "kelpie", "sirène", "golem", "minotaure"]


filename = os.path.join("nomen-summon", "bin", "species.txt")
with open(filename, "rt", encoding='utf8') as file:
    species_desc = file.readlines()
    for i, line in enumerate(species_desc):
        species_desc[i] = line.replace('\n', '')


species_zip = list(zip(species_list, species_desc))
species_dict = {index: t for index, t in enumerate(species_zip)}


# Items
item_classes = {'bmp': ('armure/bouclier', 3, 'objet'),
                'gr': ('membre', 8, 'inclassable'),
                'dnt': ('arme/outil', 8, 'objet'),
                'fvw': ('personnalisation', 0, 'autre'),
                'h': ('vêtement/accessoire', 1, 'objet'),
                'cklqx': ('source de pouvoir', 10, 'inclassable'),
                'jsz': ('familier', 5, 'autre')
                }

composed_items = {'bmp+gr': ('prothèse défensive', 11, 'objet'),
                  'bmp+dnt': ('armure équipée', 11, 'objet'),
                  'bmp+fvw': ('armure familiale', 3, 'objet'),
                  'bmp+h': ('amulette', 4, 'objet'),
                  'bmp+cklqx': ('armure de puissance', 13, 'objet'),
                  'bmp+jsz': ('armure vivante', 8, 'autre'),
                  'gr+dnt': ('prothèse offensive', 16, 'objet'),
                  'gr+fvw': ('relique', 8, 'autre'),
                  'gr+h': ('greffe', 9, 'autre'),
                  'gr+cklqx': ('membre entraîné', 18, 'autre'),
                  'gr+jsz': ('symbiote', 13, 'autre'),
                  'dnt+fvw': ('arme familiale', 8, 'objet'),
                  'dnt+h': ('belle arme', 9, 'objet'),
                  'dnt+cklqx': ('arme stimulante', 18, 'objet'),
                  'dnt+jsz': ('arme vivante', 13, 'autre'),
                  'fvw+h': ("tenue d'apparât", 1, 'objet'),
                  'fvw+cklqx': ('entraînement particulier', 10, 'inclassable'),
                  'fvw+jsz': ('esprit protecteur', 5, 'autre'),
                  'h+cklqx': ('tenue de combat', 11, 'objet'),
                  'h+jsz': ('monture', 6, 'autre'),
                  'cklqx+jsz': ('animal domestique', 15, 'autre')
                  }


items_dict = {'simple': item_classes, 'composed': composed_items}

vowels = 'aeiouy'
class_letters = l = list(vowels)
for i, v in enumerate(l[:-1]):
    next = i + 1
    class_letters.extend([v + w for w in list(vowels)[next:]])

# Classes
class_names = ['mage', 'archer', 'bretteur', 'lutteur', 'acrobate', 'technicien',
                 'aéronaute', 'paladin', 'berserker', 'danseur', 'alchimiste', 'chevalier',
                 'chasseur', 'éclaireur', 'pistolier', 'gladiateur', 'assassin', 'forgeron',
                 'artiste martial', 'médecin', 'voleur']

filename = os.path.join("nomen-summon", "bin", "classes.txt")
with open(filename, 'rt', encoding='utf8') as file:
    class_desc = file.readlines()
    for i, line in enumerate(class_desc):
        class_desc[i] = line.replace('\n', '')

class_zip = list(zip(class_letters, class_names, class_desc))
class_dict = {l: {'name': n, 'desc': d} for (l, n, d) in class_zip}

# Powers
power_names = ["saint", "élémentaliste", "chaman", "métamorphe", "téléporteur",
                "télépathe", "purificateur", "pactisant", "guérisseur", "psychopompe",
                "marionnettiste", "prophète", "druide", "météomage", "faiseur de golems",
                "avatar", "invocateur", "vaudou", "caméléon", "doppelganger", "onironaute"]

filename = os.path.join("nomen-summon", "bin", "powers.txt")
with open(filename, 'rt', encoding='utf8') as file:
    power_desc = file.readlines()
    for i, line in enumerate(power_desc):
        power_desc[i] = line.replace('\n', '')


power_letters = [l + 'n' for l in class_letters]
power_zip = list(zip(power_letters, power_names, power_desc))
power_dict = {l: {'name': n, 'desc': d} for (l, n, d) in power_zip}

aptitudes = {'classes': class_dict, 'powers': power_dict}


#   Pickle dumping functions
# You can use this script and its content to generate the pickle files again

def species():
    
    with open('species.pickle', 'wb') as species_file:
        pickle.dump(species_dict, species_file)


def items():

    with open('items.pickle', 'wb') as items_file:
        pickle.dump(items_dict, items_file)


def apts():
    

    with open('apts.pickle', 'wb') as aptitudes_file:
        pickle.dump(aptitudes, aptitudes_file)
