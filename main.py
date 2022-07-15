import bin.output as output
from bin.character import Character
from bin.utils import str_norm


# Prompts the first and last names and computes the Character object
def make_char():
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


def simple_ops():
    ch = make_char()
    print()
    output.print_char(ch)


def write_ops(filename, show=False):
    ch = make_char()
    with open(filename, 'wt', encoding='utf8') as f:
        f.write(output.print_char(ch, show))
    print(f"Fiche écrite dans {filename}")


# ### EXECUTION ####

# simple_ops()
write_ops('char.txt')
