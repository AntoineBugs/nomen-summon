import sys
import bin.output as output
from bin.character import Character
from bin.utils import str_norm
from bin.read_config import get_config


def check_args():
    args = sys.argv
    if len(args) > 1:
        if args[1] in ['-h', '--help']:
            print(output.main_usage())
            exit()
        if args[1] == '-r':
            if len(args) <= 2:
                print(output.main_usage())
                exit()
            config = args[2]
            path, mode, names = get_config(config)
            for firstN, lastN in names:
                n_path = path
                ch = make_char(firstN, lastN)
                if len(path) > 0:
                    if mode != 'at':
                        n_path = f'{firstN}_{lastN}_{n_path}'
                    write_ops(ch, n_path, mode=mode)
                else:
                    simple_ops(ch)
            exit()
        start = 1
        in_file = False
        if args[1] == '-f':
            filename = args[2]
            in_file = True
            if args[3] == '-a':
                mode = 'at'
                start = 4
            else:
                mode = 'wt'
                start = 3
        cpt = 0

        def ops(ch):
            if in_file:
                write_ops(ch, filename, mode=mode)
            else:
                simple_ops(ch)
        
        while start < len(args) and start + 1 < len(args):
            firstN = args[start]
            lastN = args[start + 1]
            ch = make_char(firstN, lastN)
            ops(ch)
            cpt += 1
            start += 2
        if cpt < 1:
            ch = make_char()
            ops(ch)
    else:
        ch = make_char()
        simple_ops(ch)
    


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


def write_ops(ch, filename, show=False, mode='wt'):
    with open(filename, mode, encoding='utf8') as f:
        f.write(output.print_char(ch, show))
    print(f"Fiche écrite dans {filename}")


# ### EXECUTION ####

check_args()
