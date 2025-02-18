from bin.data_access import find_mastery_lvl, gen_classes


def main_usage():
    """
    Returns a string that describes the usage of the main script.
    """
    s = "Usage :\n"
    lines = [
        "main.py -h | --help",
        "main.py [-f <filename> [-a]] [<full_name> [...]]",
        "\ta full_name is of the form <first_n> <last_n>.",
        "main.py -c <ref_date> [<full_name> <date> [...]]",
        "\ta date or ref_date is of the form 'YYYY-MM-DD'.",
        "main.py -r <config_file>",
    ]
    t = "\n".join(lines)
    return s + t


def item2str(item):
    """
    Convert an item dictionary to a formatted string.

    Args:
        item (dict): A dictionary containing item details with keys 'name', 'type', and 'level'.

    Returns:
        str: A formatted string representing the item.
    """
    item_str = f"\n\t· {item['name'].capitalize()}"
    if item["type"] != "inclassable":
        item_str += f" niveau {item['level']}/100"
    item_str += "\n"
    return item_str


def skill2str(skill):
    """
    Convert a skill dictionary to a formatted string.

    Args:
        skill (dict): A dictionary containing skill details with keys 'name', 'desc', 'level', and 'items'.

    Returns:
        str: A formatted string representing the skill.
    """
    name = skill["name"]
    desc = skill["desc"]
    lvl = skill["level"]
    its = skill["items"]

    s = f"· {name.capitalize()} niveau {lvl}/100 ({find_mastery_lvl(lvl)})\n"
    s += "\t" + desc + "\n"
    if len(its) > 0:
        s += "\tInventaire :"
        for it in its:
            if not it["all"]:
                s += item2str(it)
    return s


# Prints a Character object
def print_char(chara, show=True):
    """
    Prints and returns a formatted string containing information about a character.
    Args:
        chara: An object representing the character. It should have the following attributes:
            - firstN: The first name of the character.
            - familyN: The family name of the character.
            - level: The level of the character.
            - species: An object representing the species of the character, which should have:
                - species: The name of the species.
                - desc: The description of the species.
        show (bool, optional): If True, the formatted string will be printed to the console. Defaults to True.
    Returns:
        str: A formatted string containing the character's name, species, level, clan, skills, and global inventory.
    """
    fir, fam, lvl = chara.firstN, chara.familyN, chara.level
    sopt = actual_name(chara)
    sp = chara.species
    sp_n = sp.species
    # sp_d = sp.desc  #

    header = f"*** {fir} {fam}{sopt} - {sp_n.capitalize()} niveau {lvl} ***\n"
    body_spec = f"Description de l'espèce :\n\t{sp.desc}"

    body_clan = print_clan(chara)
    body_skills = print_skills(chara)
    global_inventory_str = print_global_inv(chara)
    s = "\n".join((header, body_spec, body_clan, body_skills, global_inventory_str))

    if show:
        print(s)
    return s


def print_clan(chara):
    """
    Generates a detailed description of a character's clan.
    Args:
        chara (object): The character object containing clan information.
    Returns:
        str: A formatted string containing the clan description, including
             advantages, nobility, and purity percentages.
    """
    advantages_list, adv, cl_n, cl_p = get_clan_data(chara)
    description = base_clan_desc(advantages_list, adv)

    description.append(f"\tNoblesse de lignée : {cl_n} / {percent(cl_n) * 100:.0f}%")
    description.append(f"\tPureté de lignée : {cl_p} / {percent(cl_p) * 100:.0f}%")
    description.append("")
    body_clan = "\n".join(description)
    return body_clan


def actual_name(chara):
    """
    Generate a string representing the actual name of a character.

    Args:
        chara: An object representing a character, which should have the attributes
               'act_firstN' and 'act_lastN'.

    Returns:
        A string in the format " (first_name last_name)" if both 'act_firstN' and 'act_lastN'
        are present.

    Raises:
        TypeError: If either 'act_firstN' or 'act_lastN' is missing.
    """
    sopt = ""
    if chara.act_firstN and chara.act_lastN:
        sopt = f" ({chara.act_firstN} {chara.act_lastN})"
    elif chara.act_firstN or chara.act_lastN:
        raise TypeError("Missing argument actual_firstN or actual_lastN")
    return sopt


def get_clan_data(chara):
    """
    Retrieves and processes clan data for a given character.

    Args:
        chara: An object representing a character, which contains clan information.

    Returns:
        A tuple containing:
            - advantages_list: A list of advantages derived from the character's clan gene advantages.
            - adv: A specific advantage obtained from the advantages list.
            - cl_n: The nobility attribute of the character's clan.
            - cl_p: The purity attribute of the character's clan.
    """
    clan = chara.clan
    cl_a = clan.gene_adv
    advantages_list = get_advantages(cl_a)
    adv = get_adv(advantages_list)
    cl_n, cl_p = clan.nobility, clan.purity
    return advantages_list, adv, cl_n, cl_p


def get_advantages(cl_a):
    """
    Extracts and returns a list of keys from the input dictionary where the corresponding values are greater than 1.

    Args:
        cl_a (dict): A dictionary where keys are items and values are their associated counts.

    Returns:
        list: A list of keys from the input dictionary where the values are greater than 1.
    """
    advantages_list = []
    for k, v in cl_a.items():
        if v > 1:
            advantages_list.append(k)
    return advantages_list


def get_adv(advantages_list):
    """
    Retrieves the advantages from the provided list.

    Args:
        advantages_list (list): A list of advantage keys.

    Returns:
        list: A list of advantage descriptions. If the input list is empty, returns a list containing "aucun".
    """
    adv = []
    if len(advantages_list) < 1:
        adv.append("aucun")
    else:
        for k, v in gen_classes.items():
            if k in advantages_list:
                adv.append(v)
    return adv


def percent(x):
    """
    Returns the complementary percentage of a given value x out of 26.
    """
    return (26 - x) / 26


def print_skills(chara):
    """
    Generate a formatted string of a character's skills.

    Args:
        chara (object): An object representing a character, which has an attribute 'skills' that is a list of skills.

    Returns:
        str: A formatted string listing the character's skills.
    """
    body_skills = "Aptitudes et pouvoirs :\n"
    for a in chara.skills:
        body_skills += skill2str(a) + "\n"
    return body_skills


def print_global_inv(chara):
    """
    Generates a string representation of the global inventory for a given character.

    Args:
        chara (Character): The character whose global inventory is to be printed. 
                           The character object must have a 'global_inv' attribute 
                           which is a dictionary of items.

    Returns:
        str: A string representation of the global inventory. If the inventory is 
             empty, an empty string is returned. Otherwise, the string starts with 
             "Inventaire global :" followed by the string representation of each item.
    """
    global_inventory_str = ""
    global_inv = chara.global_inv
    if global_inv:
        global_inventory_str = "Inventaire global :\n"
        for it in global_inv.values():
            global_inventory_str += item2str(it)
        global_inventory_str += "\n"
    return global_inventory_str


def base_clan_desc(advantages_list, adv):
    """
    Generates a description of a clan based on its genetic advantages.

    Args:
        advantages_list (list): A list of genetic advantages.
        adv (list): A list of advantages to be included in the description.

    Returns:
        list: A list containing the description of the clan.
    """
    description = []
    description.append("Détails du clan :")
    genetic_advantages = ", ".join(adv)
    s = "\tAvantages génétiques "
    s += ": " if len(advantages_list) <= 0 else "pour "
    s += genetic_advantages + "."
    description.append(s)
    return description
