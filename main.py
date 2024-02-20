from datetime import datetime
import sys
import bin.output as output
from bin.character import Character
from bin.utils import str_norm, vow
from bin.read_config import get_config
import chaos.seed as chs


def check_args():
    args = sys.argv
    if len(args) > 1:
        if args[1] in ["-h", "--help"]:
            print(output.main_usage())
            exit()
        if args[1] == "-c":
            if len(args) <= 2:
                print(output.main_usage())
                exit()
            year, month, day = (int(x) for x in args[2].split("-"))
            ref_date = datetime(year, month, day).date()
            chaos_args = args[3:]
            if len(chaos_args) > 1:
                start = 0
                while start + 2 < len(chaos_args):
                    firstN, lastN = chaos_args[start : start + 2]
                    year, month, day = (
                        int(x) for x in chaos_args[start + 2].split(sep="-")
                    )
                    b_date = datetime(year, month, day).date()
                    ch = make_char(firstN, lastN, birth=b_date, ref=ref_date)
                    simple_ops(ch)
                    start += 3
                exit()
            else:
                ch = make_char(ref=ref_date)
                simple_ops(ch)
                exit()
        if args[1] == "-r":
            if len(args) <= 2:
                print(output.main_usage())
                exit()
            config = args[2]
            path, mode, names = get_config(config)
            for firstN, lastN in names:
                n_path = path
                ch = make_char(firstN, lastN)
                if len(path) > 0:
                    if mode != "at":
                        n_path = f"{firstN}_{lastN}_{n_path}"
                    write_ops(ch, n_path, mode=mode)
                else:
                    simple_ops(ch)
            exit()
        start = 1
        in_file = False
        if args[1] == "-f":
            filename = args[2]
            in_file = True
            if args[3] == "-a":
                mode = "at"
                start = 4
            else:
                mode = "wt"
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
def make_char(prenom=None, nom=None, ref=None, birth=None):
    if not (prenom and nom):
        err_msg = "Votre entrée ne peut contenir que des lettres (accents permis),"
        err_msg += " des espaces et des traits d'union."

        def get_word(nature):
            w2def = True
            while w2def:
                word = input(f"Tapez {nature} et appuyez sur Entrée : ")
                w2def = not str_norm(word).isalpha()
                if w2def:
                    print(err_msg)
            return word

        prenom = get_word("un prénom")
        nom = get_word("un nom de famille")

    if ref and not birth:
        err_msg = "Votre entrée doit être au format 'YYYY-MM-DD'."
        input_msg = (
            'Tapez la date de naissance (format "YYYY-MM-DD")',
            " et appuyez sur Entrée : ",
        )
        input_msg = "".join(input_msg)
        date2def = True
        while date2def:
            date = input(input_msg)
            try:
                year, month, day = (int(x) for x in date.split(sep="-"))
                birth = datetime(year, month, day).date()
            except:  # noqa: E722
                print(err_msg)
            else:
                date2def = False

    if birth and ref:
        f_shift = chs.cos_shift(ref)
        shift = f_shift(birth.year, birth.month, birth.day)
        act_prenom, act_nom = prenom, nom
        norm_prenom, norm_nom = str_norm(prenom), str_norm(nom)
        string = "{} {}".format(norm_prenom, norm_nom)
        chl = chs.change_letters(shift, 0, 1, vow, string).split()
        size_prenom = 1
        while sum(len(s) for s in chl[:size_prenom]) < len(norm_prenom):
            size_prenom += 1
        prenom = " ".join([w.capitalize() for w in chl[:size_prenom]])
        nom = " ".join([w.capitalize() for w in chl[size_prenom:]])
        return Character(prenom, nom, act_prenom, act_nom)

    return Character(prenom, nom)


def simple_ops(ch):
    print()
    output.print_char(ch)


def write_ops(ch, filename, show=False, mode="wt"):
    with open(filename, mode, encoding="utf8") as f:
        f.write(output.print_char(ch, show))
    print(f"Fiche écrite dans {filename}")


# ### EXECUTION ####

check_args()
