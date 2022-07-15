import os
from bin.name2species import SpeciesProfile
from bin.name2clan import GeneticProfile
from bin.utils import str_norm, cut_name, label_cuts, group_cuts
from math import floor
import pickle
import output


class Character:

    def __init__(self, firstN, familyN):
        self.firstN = firstN
        self.familyN = familyN
        self.species = SpeciesProfile(self.firstN, self.familyN)
        self.clan = GeneticProfile(self.familyN)
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

        file_path = os.path.join("bin","items.pickle")
        with open(file_path, 'rb') as file:
            items = pickle.load(file)
        file_path = os.path.join("bin","apts.pickle")
        with open(file_path, 'rb') as file:
            apts = pickle.load(file)

        advantages = self.clan.gene_adv
        nobility = self.clan.nobility
        purity = self.clan.purity

        tot_skills_lvl = tot_added_values = 0

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

# ### EXECUTION ####

# simple_ops()
write_ops('char.txt')