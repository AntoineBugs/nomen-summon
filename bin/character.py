from math import floor

from bin.name2clan import GeneticProfile
from bin.name2species import SpeciesProfile
from bin.utils import cut_name, group_cuts, label_cuts
from bin.data import aptitudes as apts
from bin.data import items_dict as items


class Character:

    def __init__(self, firstN, familyN):
        self.firstN = firstN
        self.familyN = familyN
        self.species = SpeciesProfile(self.firstN, self.familyN)
        self.clan = GeneticProfile(self.familyN)
        self.advantage, self.nobility, self.purity = self.clan.get_components()
        self.tot_size, self.pow_size, self.groups = self.compute_apts()
        self.skills, self.level = self.extract_apts()

    # computes the aptitudes, their levels and inventories
    def compute_apts(self):
        name_cut = cut_name(self.firstN)
        sizes = [len(cut) for cut in name_cut]
        tot_size = sum(sizes)
        label_cut = label_cuts(name_cut)
        sizer = lambda size, label: size if label < 2 else 0
        pow_size = sum([sizer(x, y) for (x, y) in zip(sizes, label_cut)])
        groups = group_cuts(name_cut, label_cut)
        return tot_size, pow_size, groups

    # computes the aptitude levels
    def extract_apts(self):

        tot_skills_lvl = tot_added_values = 0

        skillset = []

        for group, assoc in self.groups.items():
            its = assoc['its']
            occ = assoc['occ']

            skill = {}

            if group[-1] != 'n':
                src = apts['classes']
                key = ''.join(sorted(group))
            else:
                src = apts['powers']
                key = ''.join(sorted(group[:-1])) + 'n'
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
            adv = self.key2adv(key, self.advantage)
            # advanced level
            skill['level'] = floor(adv * (its_sum + lvl))

            tot_skills_lvl += skill['level']
            tot_added_values += its_sum

            inventory = []
            for it, value_it in zip(its, values_from_its):
                spec = {
                    'name': value_it[0],
                    'type': value_it[2]
                }
                if value_it[2] != 'inclassable':
                    if value_it[2] == 'objet':
                        coeff = (53 - self.nobility) / 26
                    else:
                        coeff = (53 - self.purity) / 26
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
            if composed_key:
                act_key = find_key('+'.join(k), comp) 
                act_key += find_key('+'.join(rev(k)), comp)
            else:
                act_key = k[0]

            return act_key, composed_key

        vals = []
        for it in its:

            if len(it) == 1:
                src = items['simple']
                key = find_key(it, src)
                vals.append(src[key])
            else:
                key, composed = find_comp_key(it, items)
                if composed:
                    src = items['composed']
                    vals.append(src[key])
                else:
                    src = items['simple']
                    (n, v, t) = src[key]
                    vals.append((n, 2 * v, t))
        
        return vals

    @staticmethod
    def key2adv(key, advantages):
        adv = 1
        for c in key:
            if c != 'n':
                adv *= advantages[c]
        return adv

