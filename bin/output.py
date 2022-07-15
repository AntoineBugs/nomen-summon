# Builds a string for an aptitude 
def skill2str(skill):
    name = skill['name']
    desc = skill['desc']
    lvl = skill['level']
    its = skill['items']

    s = "· {} niveau {}\n".format(name.capitalize(), lvl)
    s += '\t' + desc + '\n'
    if len(its) > 0:
        s += "\tInventaire :"
        for it in its:
            if it['type'] != "inclassable":
                s += "\n\t· {} niveau {}".format(it['name'].capitalize(), it['level'])
            else:
                s += "\n\t· {}".format(it['name'].capitalize())

    return s


gen_classes = {
    'a': "la magie",
    'e': "l'archerie",
    "i": "l'escrime",
    "o": "la lutte",
    "u": "l'acrobatie",
    "y": "la science"
}


# Prints a Character object
def print_char(chara, show=True):
    fir, fam, lvl = chara.firstN, chara.familyN, chara.level  #
    sp = chara.species #
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

    header = f"*** {fir} {fam} - {sp_n.capitalize()} niveau {lvl} ***"
    body_spec = f"Description de l'espèce :\n\t{sp.desc}"

    l = []
    l.append("Détails du clan :")
    genetic_advantages = ', '.join(adv)
    s = "\tAvantages génétiques "
    s += ": " if len(advantages_list) <= 0 else "pour " 
    s += genetic_advantages + "."
    l.append(s)
    l.append(f"\tNoblesse de lignée : {cl_n}")
    l.append(f"\tPureté de lignée : {cl_p}")
    s = "~ Les indices de noblesse et de pureté sont situés entre 1 (pureté ou"
    s += " noblesse maximale) et 26 (pureté ou noblesse minimale) ~"
    l.append(s)
    body_clan = "\n".join(l) + "\n"

    body_skills = "Aptitudes et pouvoirs :\n"
    for a in sk:
        body_skills += skill2str(a) + '\n'

    s = '\n'.join([header, body_spec, body_clan, body_skills])
    # len_max = max(len(l) for l in s.splitlines())
    # bar = len_max*'-' + '\n'
    # print(bar + s + bar)
    if show:
        print(s)
    return s