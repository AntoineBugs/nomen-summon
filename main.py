from datetime import datetime
import sys
import bin.output as output
from bin.character import Character
from bin.utils import str_norm, vowels
from bin.read_config import get_config
import chaos.seed as chs


def check_args():
    """
    Parses command-line arguments and executes corresponding functions.

    This function checks the command-line arguments provided to the script.
    Depending on the arguments, it performs different actions:
    
    - If the first argument is '-h' or '--help', it prints the usage information and exits.
    - If the first argument is '-c', it calls the `chaos_exec` function and exits.
    - If the first argument is '-r', it calls the `read_exec` function and exits.
    - For any other arguments, it calls the `line_exec` function.
    - If no arguments are provided, it creates a character using `make_char` and performs simple operations on it using `simple_ops`.

    Note:
        This function uses `sys.argv` to get the command-line arguments and `sys.exit` to terminate the script.
    """
    args = sys.argv
    if len(args) > 1:
        if args[1] in ["-h", "--help"]:
            print(output.main_usage())
            sys.exit()
        if args[1] == "-c":
            chaos_exec(args)
            sys.exit()
        if args[1] == "-r":
            read_exec(args)
            sys.exit()
        line_exec(args)
    else:
        ch = make_char()
        simple_ops(ch)


def line_exec(args):
    """
    Executes a series of operations based on the provided arguments.
    Args:
        args (list): A list of command-line arguments. The expected format is:
            - args[1]: Optional flag "-f" to indicate file output.
            - args[2]: Filename if "-f" flag is provided.
            - args[3]: Optional flag "-a" to append to the file instead of overwriting.
            - args[4] and onwards: Pairs of arguments representing firstN and lastN.
    The function processes pairs of arguments (firstN, lastN) to create characters
    and either writes them to a file or performs simple operations on them.
    If no pairs are provided, a default character is created and processed.
    The function supports writing to a file in either write ("wt") or append ("at") mode.
    """
    start = 1
    in_file = False
    mode = "wt"  # default mode
    if args[1] == "-f":
        filename = args[2]
        in_file = True
        if args[3] == "-a":
            mode = "at"
            start = 4
        else:
            mode = "wt"
            start = 3
            start = 3
    cpt = 0

    def ops(ch):
        if in_file:
            write_ops(ch, filename, mode=mode)
        else:
            simple_ops(ch)

    while start + 1 < len(args):
        firstN = args[start]
        lastN = args[start + 1]
        ch = make_char(firstN, lastN)
        ops(ch)
        cpt += 1
        start += 2

    if cpt < 1:
        ch = make_char()
        ops(ch)


def read_exec(args):
    """
    Executes the main functionality based on the provided arguments.

    Args:
        args (list): A list of command-line arguments. The list should contain at least three elements:
            - args[0]: The script name (ignored in this function).
            - args[1]: The main command (ignored in this function).
            - args[2]: The configuration file path.

    Behavior:
        - If the length of args is less than or equal to 2, it prints the main usage information and exits.
        - Reads the configuration file specified in args[2] to get the path, mode, and names.
        - For each name (first name and last name) in the names list:
            - Creates a character using the make_char function.
            - If a path is provided:
                - If the mode is not "at", modifies the path to include the first and last names.
                - Writes the character to the specified path using write_ops.
            - If no path is provided, performs simple operations using simple_ops.
    """
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


def chaos_exec(args):
    """
    Executes the chaos command with the given arguments.

    Parameters:
    args (list): A list of command-line arguments. The list should contain at least three elements:
                 - args[0]: The script name (ignored).
                 - args[1]: The command name (ignored).
                 - args[2]: The reference date in a format that can be parsed by `date_extract`.
                 Additional elements in the list are treated as pairs of first name, last name, and birth date.

    Behavior:
    - If the length of `args` is less than or equal to 2, it prints the main usage message and exits.
    - Extracts the reference date from `args[2]`.
    - If there are additional arguments, it processes them in groups of three (first name, last name, birth date):
        - For each group, it creates a character using `make_char` with the provided names and birth date, and the reference date.
        - Performs simple operations on the created character using `simple_ops`.
    - If there are no additional arguments, it creates a character using `make_char` with only the reference date and performs simple operations on it.
    - Exits the program after processing.
    """
    if len(args) <= 2:
        print(output.main_usage())
        exit()
    ref_date = date_extract(args[2])
    chaos_args = args[3:]
    if len(chaos_args) > 1:
        start = 0
        while start + 2 < len(chaos_args):
            firstN, lastN = chaos_args[start : start + 2]
            b_date = date_extract(chaos_args[start + 2])
            ch = make_char(firstN, lastN, birth=b_date, ref=ref_date)
            simple_ops(ch)
            start += 3
        exit()
    else:
        ch = make_char(ref=ref_date)
        simple_ops(ch)
        exit()


# Prompts the first and last names and computes the Character object
def make_char(prenom=None, nom=None, ref=None, birth=None):
    """
    Creates a Character object with the given parameters.
    If `prenom` and `nom` are not provided, they will be generated using the `get_names` function.
    If `ref` is provided and `birth` is not, `birth` will be generated using the `get_birth` function.
    If both `ref` and `birth` are provided, the names will be shifted using the `shift_names` function.
    Args:
        prenom (str, optional): The first name of the character. Defaults to None.
        nom (str, optional): The last name of the character. Defaults to None.
        ref (str, optional): A reference value used for shifting names. Defaults to None.
        birth (str, optional): The birth date used for shifting names. Defaults to None.
    Returns:
        Character: A Character object with the specified or generated names.
    """
    if not (prenom and nom):
        prenom, nom = get_names()

    if ref and not birth:
        birth = get_birth()

    if birth and ref:
        prenom, nom, act_prenom, act_nom = shift_names(prenom, nom, ref, birth)
        return Character(prenom, nom, act_prenom, act_nom)

    return Character(prenom, nom)


def get_names():
    """
    Prompts the user to input a first name and a last name, ensuring that the inputs
    contain only letters (including accents), spaces, and hyphens.
    Returns:
        tuple: A tuple containing the first name and last name as strings.
    """
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
    return prenom, nom


def get_birth():
    """
    Prompts the user to input their birth date in the format 'YYYY-MM-DD' and validates the input.

    Returns:
        datetime.date: The birth date extracted from the user's input.

    Raises:
        ValueError: If the input is not in the correct format or cannot be parsed as a date.
    """
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
            birth = date_extract(date)
        except:  # noqa: E722
            print(err_msg)
        else:
            date2def = False
    return birth


def shift_names(prenom, nom, ref, birth):
    """
    Shifts the given first name (prenom) and last name (nom) based on a reference value (ref) and birth date (birth).

    Args:
        prenom (str): The first name to be shifted.
        nom (str): The last name to be shifted.
        ref (any): A reference value used to calculate the shift.
        birth (datetime.date): The birth date used in the shift calculation.

    Returns:
        tuple: A tuple containing:
            - prenom (str): The shifted first name.
            - nom (str): The shifted last name.
            - act_prenom (str): The original first name.
            - act_nom (str): The original last name.
    """
    cosine_shift_function = chs.cos_shift(ref)
    shift = cosine_shift_function(birth.year, birth.month, birth.day)
    act_prenom, act_nom = prenom, nom
    norm_prenom, norm_nom = str_norm(prenom), str_norm(nom)
    string = f"{norm_prenom} {norm_nom}"
    chl = chs.change_letters(shift, 0, 1, vowels, string).split()
    size_prenom = 1
    while sum(len(s) for s in chl[:size_prenom]) < len(norm_prenom):
        size_prenom += 1
    prenom = " ".join([w.capitalize() for w in chl[:size_prenom]])
    nom = " ".join([w.capitalize() for w in chl[size_prenom:]])
    return prenom, nom, act_prenom, act_nom


def date_extract(date):
    """
    Extracts a date from a string in the format 'YYYY-MM-DD'.

    Args:
        date (str): A string representing a date in the format 'YYYY-MM-DD'.

    Returns:
        datetime.date: A date object representing the extracted date.
    """
    year, month, day = (int(x) for x in date.split(sep="-"))
    birth = datetime(year, month, day).date()
    return birth


def simple_ops(ch):
    """
    Perform a simple operation by printing a character.

    Args:
        ch (str): The character to be printed.
    """
    print()
    output.print_char(ch)


def write_ops(ch, filename, show=False, mode="wt"):
    """
    Writes the output of a character to a file.

    Args:
        ch (str): The character to be written.
        filename (str): The name of the file where the character will be written.
        show (bool, optional): If True, additional information about the character will be shown. Defaults to False.
        mode (str, optional): The mode in which the file is opened. Defaults to "wt".
    """
    with open(filename, mode, encoding="utf8") as f:
        f.write(output.print_char(ch, show))
    print(f"Fiche écrite dans {filename}")


# ### EXECUTION ####

check_args()
