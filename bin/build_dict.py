import pickle

# You use this script and its content to generate the pickle files again

species_list = ["loup-garou", "ange", "orc", "harpie", "dragonide", "gobelin", "nain",
                "faune", "elfe", "félice", "vampire", "reptilien", "géant", "humain",
                "démon", "naga", "fée", "féloure", "selkie", "gnome", "centaure",
                "troll", "kelpie", "sirène", "golem", "minotaure"]

desc = [
    "Les loups-garous adoptent en général une apparence humaine, mais peuvent se transformer (notamment lors des "
    "nuits de pleine lune) en énormes loups.",
    "Les anges ne diffèrent des humains que par une paire d'ailes de plus ou moins grande envergure dans leur dos, "
    "leur permettant de voler.",
    "Les orcs sont de grands êtres humanoïdes à la peau verte ou grise, aux oreilles pointues et aux yeux sombres.",
    "Les harpies sont de véritables hybrides entre des humains et des oiseaux, ayant des ailes à la place des bras et "
    "des pattes munies de serres pour jambes.",
    "Les dragonides peuvent alterner entre une forme de dragon et une forme humaine pouvant conserver certain des "
    "traits de l'autre forme (queue, écailles, cornes ...).",
    "Les gobelins sont de petits êtres humanoïdes à la peau verte ou grise, aux oreilles pointues et aux yeux sombres.",
    "Les nains ressemblent à des humains, mais ont un corps généralement plus petit et trapu, et une force physique "
    "supérieure.",
    "Les faunes ont une apparence majoritairement humaine, mais aussi des cornes et des pattes de bouc ou chèvre en "
    "guise de jambes.",
    "Les elfes se distinguent des humains par des oreilles pointues, une taille moyenne plus importante et une grande "
    "longévité.",
    "Les félices ont des traits plutôt proches du chat, mais une apparence humanoïde.",
    "Les vampires ont une peau pâle et très sensible à la lumière, des canines surdéveloppées et une grande longévité.",
    "Les reptiliens ont des traits plutôt proches du lézard, mais une apparence humanoïde.",
    "Les géants ont une apparence humaine, mais une taille beaucoup plus importante.",
    "Les humains sont ... humanoïdes.",
    "Les démons ont une apparence humaine, couplée à des cornes de diverses formes et une queue.",
    "Les nagas ont un buste humain sur un corps de serpent.",
    "Les fées sont semblables aux humains, à quelques différences près : une plus petite taille, des ailes d'insectes "
    "et des oreilles en pointe.",
    "Les féloures ont des traits plutôt proches du panda géant, mais une apparence humanoïde.",
    "Les selkies sont des humains capables de se transformer en phoques grâce à une seconde peau.",
    "Les gnomes ont une apparence humanoïde, mais une très petite taille et des oreilles en pointe.",
    "Les centaures ont un buste humain sur un corps de cheval.",
    "Les trolls sont de très grandes créatures humanoïdes à la peau grise et dure comme la pierre.",
    "Les kelpies vivent dans des lacs et peuvent alterner entre une forme humaine et une forme de cheval.",
    "Les sirènes ont un buste humain sur un corps de poisson.",
    "Les golems sont des statues - généralement d'argile - qui ont pris vie.",
    "Les minotaures ont les traits d'une vache ou d'un taureau, mais une apparence humanoïde."
]


def species():
    cumulated = {index: (x, desc[index]) for index, x in enumerate(species_list)}

    with open('species.pickle', 'wb') as species_file:
        pickle.dump(cumulated, species_file)


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


def items():
    d = {'simple': item_classes,
         'composed': composed_items}

    with open('items.pickle', 'wb') as items_file:
        pickle.dump(d, items_file)


classes_letters = 'a e i o u y ae ai ao au ay ei eo eu ey io iu iy ou oy uy'.split(' ')

classes_names = ['mage', 'archer', 'bretteur', 'lutteur', 'acrobate', 'technicien',
                 'aéronaute', 'paladin', 'berserker', 'danseur', 'alchimiste', 'chevalier',
                 'chasseur', 'éclaireur', 'pistolier', 'gladiateur', 'assassin', 'forgeron',
                 'artiste martial', 'médecin', 'voleur']

with open('classes.txt', 'rt') as file:
    classes_desc = file.readlines()
    for i, line in enumerate(classes_desc):
        classes_desc[i] = line.replace('\n', '')

powers_names = ["saint", "élémentaliste", "chaman", "métamorphe", "téléporteur",
                "télépathe", "purificateur", "pactisant", "guérisseur", "psychopompe",
                "marionnettiste", "prophète", "druide", "météomage", "faiseur de golems",
                "avatar", "invocateur", "vaudou", "caméléon", "doppelganger", "onironaute"]

with open('powers.txt', 'rt') as file:
    powers_desc = file.readlines()
    for i, line in enumerate(powers_desc):
        powers_desc[i] = line.replace('\n', '')


def apts():
    class_dict = {l: {'name': classes_names[index], 'desc': classes_desc[index]} for index, l in enumerate(
        classes_letters)}
    power_dict = {l + 'n': {'name': powers_names[index], 'desc': powers_desc[index]} for index, l in enumerate(
        classes_letters)}
    aptitudes = {'classes': class_dict, 'powers': power_dict}

    with open('apts.pickle', 'wb') as aptitudes_file:
        pickle.dump(aptitudes, aptitudes_file)
