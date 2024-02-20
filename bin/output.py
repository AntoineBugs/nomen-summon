from bin.data_access import find_mastery_lvl


def main_usage():
    s = "Usage :\n"
    lines = [
        "main.py -h | --help",
        "main.py [-f <filename> [-a]] [<full_name> [<full_name_2> ...]]",
        "\ta full_name is of the form <first_n> <last_n>.",
        "main.py -c <ref_date> [<full_name> <date> [<full_name_2> <date_2> ...]]"
        "\ta date or ref_date is of the form 'YYYY-MM-DD'.",
        "main.py -r <config_file>",
    ]
    t = "\n".join(lines)
    return s + t


def item2str(item):
    s = f"\n\t· {item['name'].capitalize()}"
    if item["type"] != "inclassable":
        s += f" niveau {item['level']}/100"
    s += "\n"
    return s


# Builds a string for an aptitude
def skill2str(skill):
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


gen_classes = {
    "a": "la magie",
    "e": "l'archerie",
    "i": "l'escrime",
    "o": "la lutte",
    "u": "l'acrobatie",
    "y": "la science",
}


# Prints a Character object
def print_char(chara, show=True):
    fir, fam, lvl = chara.firstN, chara.familyN, chara.level  #
    sopt = ""
    if chara.act_firstN and chara.act_lastN:
        sopt = f" ({chara.act_firstN} {chara.act_lastN})"
    elif chara.act_firstN or chara.act_lastN:
        raise TypeError("Missing argument actual_firstN or actual_lastN")
    sp = chara.species  #
    sp_n = sp.species  #
    # sp_d = sp.desc  #

    clan = chara.clan  #
    cl_a = clan.gene_adv  #
    advantages_list = []
    for k, v in cl_a.items():
        if v > 1:
            advantages_list.append(k)
    adv = []
    if len(advantages_list) < 1:
        adv.append("aucun")
    else:
        for k, v in gen_classes.items():
            if k in advantages_list:
                adv.append(v)
    cl_n, cl_p = clan.nobility, clan.purity  #

    sk = chara.skills

    header = f"*** {fir} {fam}{sopt} - {sp_n.capitalize()} niveau {lvl} ***\n"
    body_spec = f"Description de l'espèce :\n\t{sp.desc}"

    description = []
    description.append("Détails du clan :")
    genetic_advantages = ", ".join(adv)
    s = "\tAvantages génétiques "
    s += ": " if len(advantages_list) <= 0 else "pour "
    s += genetic_advantages + "."
    description.append(s)

    def percent(x):
        return (26 - x) / 26

    description.append(f"\tNoblesse de lignée : {cl_n} / {percent(cl_n):.0%}")
    description.append(f"\tPureté de lignée : {cl_p} / {percent(cl_p):.0%}")
    # s = "~ Les indices de noblesse et de pureté sont situés entre 1 (pureté"
    # s += " ou noblesse maximale) et 26 (pureté ou noblesse minimale) ~"
    # l.append(s)
    body_clan = "\n".join(description) + "\n"

    body_skills = "Aptitudes et pouvoirs :\n"
    for a in sk:
        body_skills += skill2str(a) + "\n"

    body_global_inv = ""
    global_inv = chara.global_inv
    if len(global_inv.keys()) > 0:
        body_global_inv = "Inventaire global :"
        for it in global_inv.values():
            body_global_inv += item2str(it)
        body_global_inv += "\n"

    s = "\n".join([header, body_spec, body_clan, body_skills, body_global_inv])

    if show:
        print(s)
    return s
