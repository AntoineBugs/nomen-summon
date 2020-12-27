import bin.name2species as nts
import bin.name2clan as ntc
from bin.utils import str_norm, cut_name, label_cuts, group_cuts
from math import floor
import pickle


class Character:

    def __init__(self, firstN, familyN):
        self.firstN = firstN
        self.familyN = familyN
        self.species = nts.SpeciesProfile(self.firstN, self.familyN)
        self.clan = ntc.GeneticProfile(self.familyN)
        self.tot_size, self.pow_size, self.groups = self.compute_apts()
        self.skills, self.level = self.extract_apts()

    # computes the aptitudes, their levels and inventories
    def compute_apts(self):
        name_cut = cut_name(self.firstN)
        sizes = [len(cut) for cut in name_cut]
        tot_size = sum(sizes)
        label_cut = label_cuts(name_cut)
        pow_size = sum([size if label < 2 else 0 for (size, label) in zip(sizes, label_cut)])
        groups = group_cuts(name_cut, label_cut)
        return tot_size, pow_size, groups

    # computes the aptitude levels
    def extract_apts(self):

        with open('bin/items.pickle', 'rb') as file:
            items = pickle.load(file)
        with open('bin/apts.pickle', 'rb') as file:
            apts = pickle.load(file)

        advantages = self.clan.gene_adv
        nobility = self.clan.nobility
        purity = self.clan.purity

        tot_skills_lvl = 0
        tot_added_values = 0

        skillset = []

        for group, assoc in self.groups.items():
            its = assoc['its']
            occ = assoc['occ']

            skill = {}

            src = apts['classes'] if group[-1] != 'n' else apts['powers']
            key = ''.join(sorted(group)) if group[-1] != 'n' else ''.join(sorted(group[:-1])) + 'n'
            apt = src[key]
            skill['name'] = apt['name']
            skill['desc'] = apt['desc']

            size = occ * len(key)
            # base level
            lvl = 100 * size / self.pow_size
            # items added value
            values_from_its = self.extract_items(its, items)
            its_sum = sum([it[1] for it in values_from_its])
            # genetic advantage
            adv = self.key2adv(key, advantages)
            # advanced level
            skill['level'] = floor(adv * (its_sum + lvl))

            tot_skills_lvl += skill['level']
            tot_added_values += its_sum

            inventory = []
            for it, value_it in zip(its, values_from_its):
                spec = {'name': value_it[0], 'type': value_it[2]}
                if value_it[2] != 'inclassable':
                    coeff = 53 - (nobility if value_it[2] == 'objet' else purity)
                    coeff /= 26
                    size = len(it)
                    spec['level'] = floor(100 * coeff * size / self.pow_size)
                inventory.append(spec)

            skill['items'] = inventory

            skillset.append(skill)

        skill_part = tot_skills_lvl / 100
        skill_part += 1

        remainder = 100 * (self.tot_size - self.pow_size) / self.pow_size
        remainder += 100 + tot_added_values

        level = floor(skill_part * remainder)

        return skillset, level

    # computes the item levels
    @staticmethod
    def extract_items(its, items):

        def find_key(item, source):
            key_list = [k if item in k else '' for k in source.keys()]
            return ''.join(key_list)

        def find_comp_key(item, inventory):

            def rev(list_to_reverse):
                nl = list_to_reverse.copy()
                nl.reverse()
                return nl

            simple = inventory['simple']
            comp = inventory['composed']
            k = [find_key(c, simple) for c in item]
            composed_key = k[0] != k[1]
            act_key = find_key('+'.join(k), comp) + find_key('+'.join(rev(k)), comp) if composed_key else k[0]

            return act_key, composed_key

        val = []
        for it in its:
            if len(it) == 1:
                src = items['simple']
                key = find_key(it, src)
                val.append(src[key])
            else:
                key, composed = find_comp_key(it, items)
                if composed:
                    src = items['composed']
                    val.append(src[key])
                else:
                    src = items['simple']
                    (n, v, t) = src[key]
                    val.append((n, 2 * v, t))
        return val

    @staticmethod
    def key2adv(key, advantages):
        adv = 1
        for c in key:
            if c != 'n':
                adv *= advantages[c]
        return adv


# Prompts the first and last names and computes the Character object
def make_char():
    err_msg = "Votre entrée ne peut contenir que des lettres (accents permis), des espaces et des traits d'union."
    prenom, nom = "", ""

    p2def = True
    while p2def:
        prenom = input('Tapez un prénom et appuyez sur Entrée : ')
        p2def = not str_norm(prenom).isalpha()
        if p2def:
            print(err_msg)
    n2def = True
    while n2def:
        nom = input('Tapez un nom de famille et appuyez sur Entrée : ')
        n2def = not str_norm(nom).isalpha()
        if n2def:
            print(err_msg)
    return Character(prenom, nom)


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


# Prints a Character object
def print_char(chara):
    fir = chara.firstN  #
    fam = chara.familyN  #
    lvl = chara.level  #

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
        if 'a' in advantages_list:
            adv.append("la magie")
        if 'e' in advantages_list:
            adv.append("l'archerie")
        if 'i' in advantages_list:
            adv.append("l'escrime")
        if 'o' in advantages_list:
            adv.append("la lutte")
        if 'u' in advantages_list:
            adv.append("l'acrobatie")
        if 'y' in advantages_list:
            adv.append("la science")
    cl_n = clan.nobility  #
    cl_p = clan.purity  #

    sk = chara.skills

    header = "*** {} {} - {} niveau {} ***".format(fir, fam, sp_n.capitalize(), lvl)
    body_spec = "Description de l'espèce :\n\t{}".format(sp.desc)

    body_clan = "Détails du clan :\n"
    genetic_advantages = ', '.join(adv)
    body_clan += "\tAvantages génétiques " + (
        ": " if len(advantages_list) <= 0 else "pour ") + genetic_advantages + ".\n "
    body_clan += "\tNoblesse de lignée : {}\n".format(cl_n)
    body_clan += "\tPureté de lignée : {}\n".format(cl_p)
    body_clan += "~ Les indices de noblesse et de pureté sont situés entre 1 (pureté ou noblesse maximale) et 26 (" \
                 "pureté ou noblesse minimale) ~\n "

    body_skills = "Aptitudes et pouvoirs :\n"
    for a in sk:
        body_skills += skill2str(a) + '\n'

    s = '\n'.join([header, body_spec, body_clan, body_skills])
    # len_max = max(len(l) for l in s.splitlines())
    # bar = len_max*'-' + '\n'
    # print(bar + s + bar)
    print(s)


# ### EXECUTION ####

ch = make_char()
print()
print_char(ch)
