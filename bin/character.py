from math import floor

from bin.name2clan import GeneticProfile
from bin.name2species import SpeciesProfile
from bin.utils import cut_name, group_cuts, label_cuts
from data.data import aptitudes as apts, items_dict as items


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

    def compute_apts(self):
        """
        Computes various attributes for the character based on their first name.
        This method performs the following computations:
        1. Cuts the first name into segments.
        2. Calculates the size of each segment and the total size.
        3. Labels each segment.
        4. Computes the power size based on segment sizes and labels.
        5. Groups the segments and creates a global inventory.
        Attributes:
            self.firstN (str): The first name of the character.
            self.tot_size (int): The total size of all name segments.
            self.pow_size (int): The power size, which is the sum of sizes of segments with a label less than 2.
            self.groups (list): The grouped segments of the name.
            self.global_inv (dict): A dictionary representing the global inventory of segments.
        """
        name_cut = cut_name(self.firstN)
        sizes = [len(cut) for cut in name_cut]
        self.tot_size = sum(sizes)
        label_cut = label_cuts(name_cut)

        def sizer(size, label):
            return size if label < 2 else 0

        self.pow_size = sum([sizer(x, y) for (x, y) in zip(sizes, label_cut)])
        self.groups, global_inv = group_cuts(name_cut, label_cut)
        self.global_inv = {x: {} for x in global_inv}

    def extract_apts(self):
        """
        Extracts the aptitudes (skills and levels) of the character.
        This method initializes the total skill levels and added values to zero,
        then iterates through the character's groups to update the skillset.
        Finally, it retrieves the character's level.
        Returns:
            tuple: A tuple containing the skillset (list) and the character's level (int).
        """
        self.tot_skills_lvl = self.tot_added_values = 0
        skillset = []

        for group, assoc in self.groups.items():
            self.update_skillset(skillset, group, assoc)

        level = self.get_level()

        return skillset, level

    def get_level(self):
        """
        Calculate the character's level based on their skills and size attributes.
        The level is determined by a combination of the total skill levels, 
        the total size, the power size, and any additional values.
        Returns:
            int: The calculated level of the character.
        """
        skill_part = self.tot_skills_lvl / 100
        skill_part += 1

        remainder = 100 * (self.tot_size - self.pow_size) / self.pow_size
        remainder += 100 + self.tot_added_values

        level = floor(skill_part * remainder)
        return level

    def update_skillset(self, skillset, group, assoc):
        """
        Updates the skillset of a character by computing and adding a new skill based on the provided associations.
        Args:
            skillset (list): The list of skills to be updated.
            group (str): The group identifier used to find the appropriate skill.
            assoc (dict): A dictionary containing associations with keys:
                - "its" (list): A list of items.
                - "occ" (list): A list of occurrences.
                - "globals" (dict): A dictionary of global values.
        """
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
        """
        Computes the levels based on items, occupation, skill, and key.

        Args:
            its (list): List of items.
            occ (int): Occupation value.
            skill (dict): Dictionary containing skill information.
            key (str): Key used for computation.

        Returns:
            tuple: A tuple containing:
                - values_from_its (list): List of extracted items with their values.
                - its_sum (int): Sum of the values from the extracted items.
        """
        size = occ * len(key)
        lvl = 100 * size / self.pow_size  # base level
        values_from_its = self.extract_items(its, items)
        its_sum = sum([it[1] for it in values_from_its])  # items added value
        adv = self.key2adv(key, self.advantage)  # genetic advantage
        skill["level"] = floor(adv * (its_sum + lvl))  # advanced level
        return values_from_its, its_sum

    def find_apt(self, group, skill):
        """
        Finds and assigns the appropriate aptitude information to the given skill.

        Args:
            group (str): The group identifier for the aptitude. If the last character is 'n', it indicates a power group.
            skill (dict): The skill dictionary to which the aptitude information will be assigned.

        Returns:
            str: The key used to retrieve the aptitude information from the source.
        """
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
        """
        Generates an inventory list based on provided items, global flags, and item values.

        Args:
            its (list): List of items.
            globals (list): List of boolean flags indicating if the item is global.
            values_from_its (list): List of item values, where each value is a list containing
                                    the item's name, type, and other attributes.

        Returns:
            list: A list of dictionaries, each representing an item with its specifications.
                  Each dictionary contains the following keys:
                  - 'name': The name of the item.
                  - 'type': The type of the item.
                  - 'all': Boolean flag indicating if the item is global.
                  - 'level' (optional): The calculated level of the item based on its type and size.
        """
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
        """
        Extracts values from a list of items based on the provided iterable.
        Args:
            its (iterable): An iterable containing elements to be processed.
            items (list): A list of items from which values will be extracted.
        Returns:
            list: A list of extracted values.
        """
        vals = []
        for it in its:
            Character.update_vals(items, vals, it)

        return vals

    @staticmethod
    def find_key(item, source):
        """
        Finds and returns the key from the source dictionary that contains the specified item.

        Args:
            item (str): The item to search for within the keys of the source dictionary.
            source (dict): The dictionary to search through.

        Returns:
            str: The key that contains the item. If no key contains the item, returns an empty string.
        """
        key_list = [k if item in k else "" for k in source.keys()]
        return "".join(key_list)

    @staticmethod
    def find_comp_key(item, inventory):
        """
        Finds the composed key for a given item in the inventory.
        Args:
            item (list): A list of characters/items to find the key for.
            inventory (dict): A dictionary containing 'simple' and 'composed' keys with their respective inventories.
        Returns:
            tuple: A tuple containing the found key and a boolean indicating if the key is composed.
        """
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
        """
        Updates the vals list based on the provided items and it (iterator).

        Args:
            items (dict): A dictionary containing "simple" and "composed" items.
            vals (list): A list to be updated with values from items.
            it (iterator): An iterator used to find keys in the items dictionary.

        Returns:
            None: This function updates the vals list in place.

        Notes:
            - If the length of it is 1, the function looks for the key in the "simple" items.
            - If the length of it is greater than 1, the function determines if the key is in "composed" or "simple" items.
            - If the key is in "simple" items and not composed, the value is modified before being appended to vals.
        """
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
        """
        Calculate the product of advantages based on the given key.

        Args:
            key (str): A string where each character represents a key to an advantage.
            advantages (dict): A dictionary where keys are characters and values are the corresponding advantage values.

        Returns:
            int: The product of the advantage values for each character in the key, excluding 'n'.
        """
        adv = 1
        for c in key:
            if c != "n":
                adv *= advantages[c]
        return adv
