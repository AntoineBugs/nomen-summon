import sys
import bin.output as output
from bin.character import Character
from bin.utils import str_norm


# Prompts the first and last names and computes the Character object
def make_char(prenom=None, nom=None):
    if prenom is None or nom is None:
        err_msg = "Votre entrée ne peut contenir que des lettres (accents permis),"
        err_msg += " des espaces et des traits d'union."
        
        def get_word(nature):
            w2def = True
            while w2def:
                word = input(f'Tapez {nature} et appuyez sur Entrée : ')
                w2def = not str_norm(word).isalpha()
                if w2def:
                    print(err_msg)
            return word
        
        prenom = get_word("un prénom")
        nom = get_word("un nom de famille")
    return Character(prenom, nom)


def simple_ops(ch):
    print()
    output.print_char(ch)


def write_ops(ch, filename, show=False):
    with open(filename, 'wt', encoding='utf8') as f:
        f.write(output.print_char(ch, show))
    print(f"Fiche écrite dans {filename}")


# ### EXECUTION ####

filename = "char.txt"
args = sys.argv
if len(args) > 1:
    if args[1] in ['-h', '--help'] or len(args) not in [3, 5]:
        print(output.main_usage())
        exit()
    start = 1
    in_file = False
    if args[1] == '-f':
        filename = args[2]
        start = 3
        in_file = True
    firstN = lastN = None
    if start + 1 < len(args):
        firstN = args[start]
        lastN = args[start + 1]
    ch = make_char(firstN, lastN)
    write_ops(ch, filename) if in_file else simple_ops(ch)
else:
    ch = make_char()
    simple_ops(ch)
