from math import floor

from bin.name2clan import GeneticProfile
from bin.name2species import SpeciesProfile
from bin.utils import cut_name, group_cuts, label_cuts
from bin.data_access import aptitudes as apts
from bin.data_access import items_dict as items


class Character:
    def __init__(self, firstN, familyN, act_firstN=None, act_lastN=None):
        self.firstN = firstN
        self.familyN = familyN
        self.act_firstN = act_firstN
        self.act_lastN = act_lastN
        self.species = SpeciesProfile(self.firstN, self.familyN)
        self.clan = GeneticProfile(self.familyN)
        self.advantage, self.nobility, self.purity = self.clan.get_components()
        self.compute_apts()
        self.skills, self.level = self.extract_apts()

    # computes the aptitudes, their levels and inventories
    def compute_apts(self):
        name_cut = cut_name(self.firstN)
        sizes = [len(cut) for cut in name_cut]
        self.tot_size = sum(sizes)
        label_cut = label_cuts(name_cut)

        def sizer(size, label):
            return size if label < 2 else 0

        self.pow_size = sum([sizer(x, y) for (x, y) in zip(sizes, label_cut)])
        self.groups, global_inv = group_cuts(name_cut, label_cut)
        self.global_inv = {x: {} for x in global_inv}

    # computes the aptitude levels
    def extract_apts(self):
        self.tot_skills_lvl = self.tot_added_values = 0
        skillset = []

        for group, assoc in self.groups.items():
            self.update_skillset(skillset, group, assoc)

        level = self.get_level()

        return skillset, level

    def get_level(self):
        skill_part = self.tot_skills_lvl / 100
        skill_part += 1

        remainder = 100 * (self.tot_size - self.pow_size) / self.pow_size
        remainder += 100 + self.tot_added_values

        level = floor(skill_part * remainder)
        return level

    def update_skillset(self, skillset, group, assoc):
        its, occ = assoc["its"], assoc["occ"]
        globals = assoc["globals"]

        skill = {}
        key = self.find_apt(group, skill)
        values_from_its, its_sum = self.compute_levels(its, occ, skill, key)

        self.tot_skills_lvl += skill["level"]
        self.tot_added_values += its_sum
        skill["items"] = self.get_inventory(its, globals, values_from_its)

        skillset.append(skill)

    def compute_levels(self, its, occ, skill, key):
        size = occ * len(key)
        lvl = 100 * size / self.pow_size  # base level
        values_from_its = self.extract_items(its, items)
        its_sum = sum([it[1] for it in values_from_its])  # items added value
        adv = self.key2adv(key, self.advantage)  # genetic advantage
        skill["level"] = floor(adv * (its_sum + lvl))  # advanced level
        return values_from_its, its_sum

    def find_apt(self, group, skill):
        if group[-1] != "n":
            src = apts["classes"]
            key = "".join(sorted(group))
        else:
            src = apts["powers"]
            key = "".join(sorted(group[:-1])) + "n"
        apt = src[key]
        for k in "name", "desc":
            skill[k] = apt[k]
        return key

    def get_inventory(self, its, globals, values_from_its):
        inventory = []
        for it, value_it, glob in zip(its, values_from_its, globals):
            spec = dict(name=value_it[0], type=value_it[2], all=glob)
            if value_it[2] != "inclassable":
                if value_it[2] == "objet":
                    coeff = (53 - self.nobility) / 26
                else:
                    coeff = (53 - self.purity) / 26
                size = len(it)
                spec["level"] = floor(100 * coeff * size / self.pow_size)
            inventory.append(spec)
            if glob:
                self.global_inv[it] = spec
        return inventory

    # computes the item levels
    @staticmethod
    def extract_items(its, items):
        vals = []
        for it in its:
            Character.update_vals(items, vals, it)

        return vals

    @staticmethod
    def find_key(item, source):
        key_list = [k if item in k else "" for k in source.keys()]
        return "".join(key_list)

    @staticmethod
    def find_comp_key(item, inventory):
        def rev(list_to_reverse):
            nl = list_to_reverse.copy()
            nl.reverse()
            return nl

        simple = inventory["simple"]
        comp = inventory["composed"]
        k = [Character.find_key(c, simple) for c in item]
        composed_key = k[0] != k[1]
        if composed_key:
            act_key = Character.find_key("+".join(k), comp)
            act_key += Character.find_key("+".join(rev(k)), comp)
        else:
            act_key = k[0]

        return act_key, composed_key

    @staticmethod
    def update_vals(items, vals, it):
        if len(it) == 1:
            src = items["simple"]
            key = Character.find_key(it, src)
            vals.append(src[key])
        else:
            key, composed = Character.find_comp_key(it, items)
            if composed:
                src = items["composed"]
                vals.append(src[key])
            else:
                src = items["simple"]
                (n, v, t) = src[key]
                vals.append((n, 2 * v, t))

    @staticmethod
    def key2adv(key, advantages):
        adv = 1
        for c in key:
            if c != "n":
                adv *= advantages[c]
        return adv
