from bin.data_access import find_mastery_lvl, gen_classes


def main_usage():
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


# Prints a Character object
def print_char(chara, show=True):
    fir, fam, lvl = chara.firstN, chara.familyN, chara.level  #
    sopt = actual_name(chara)
    sp = chara.species  #
    sp_n = sp.species  #
    # sp_d = sp.desc  #

    header = f"*** {fir} {fam}{sopt} - {sp_n.capitalize()} niveau {lvl} ***\n"
    body_spec = f"Description de l'espèce :\n\t{sp.desc}"

    body_clan = print_clan(chara)
    body_skills = print_skills(chara)
    body_global_inv = print_global_inv(chara)

    s = "\n".join([header, body_spec, body_clan, body_skills, body_global_inv])

    if show:
        print(s)
    return s


def print_clan(chara):
    advantages_list, adv, cl_n, cl_p = get_clan_data(chara)
    description = base_clan_desc(advantages_list, adv)

    description.append(f"\tNoblesse de lignée : {cl_n} / {percent(cl_n):.0%}")
    description.append(f"\tPureté de lignée : {cl_p} / {percent(cl_p):.0%}")
    description.append("")
    body_clan = "\n".join(description)
    return body_clan


def actual_name(chara):
    sopt = ""
    if chara.act_firstN and chara.act_lastN:
        sopt = f" ({chara.act_firstN} {chara.act_lastN})"
    elif chara.act_firstN or chara.act_lastN:
        raise TypeError("Missing argument actual_firstN or actual_lastN")
    return sopt


def get_clan_data(chara):
    clan = chara.clan  #
    cl_a = clan.gene_adv  #
    advantages_list = get_advantages(cl_a)
    adv = get_adv(advantages_list)
    cl_n, cl_p = clan.nobility, clan.purity
    return advantages_list, adv, cl_n, cl_p


def get_advantages(cl_a):
    advantages_list = []
    for k, v in cl_a.items():
        if v > 1:
            advantages_list.append(k)
    return advantages_list


def get_adv(advantages_list):
    adv = []
    if len(advantages_list) < 1:
        adv.append("aucun")
    else:
        for k, v in gen_classes.items():
            if k in advantages_list:
                adv.append(v)
    return adv


def percent(x):
    return (26 - x) / 26


def print_skills(chara):
    body_skills = "Aptitudes et pouvoirs :\n"
    for a in chara.skills:
        body_skills += skill2str(a) + "\n"
    return body_skills


def print_global_inv(chara):
    body_global_inv = ""
    global_inv = chara.global_inv
    if len(global_inv.keys()) > 0:
        body_global_inv = "Inventaire global :"
        for it in global_inv.values():
            body_global_inv += item2str(it)
        body_global_inv += "\n"
    return body_global_inv


def base_clan_desc(advantages_list, adv):
    description = []
    description.append("Détails du clan :")
    genetic_advantages = ", ".join(adv)
    s = "\tAvantages génétiques "
    s += ": " if len(advantages_list) <= 0 else "pour "
    s += genetic_advantages + "."
    description.append(s)
    return description
