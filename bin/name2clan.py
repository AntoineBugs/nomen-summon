from bin.utils import str_norm


def wipe_letter(s, c):
    """
    Remove all occurrences of a specified character from a string.

    Args:
        s (str): The input string from which the character will be removed.
        c (str): The character to be removed from the input string.

    Returns:
        str: A new string with all occurrences of the specified character removed.
    """
    new = ''.join(s.split(c))
    return new


def wipe_outer(s):
    """
    Removes the first and last characters from the input string `s` and 
    then removes any occurrences of these characters from the resulting string.

    Args:
        s (str): The input string to be processed.

    Returns:
        str: The processed string with the first and last characters removed 
             and any occurrences of these characters removed from the resulting string.
    """
    beg = s[0]
    end = s[-1]
    new = wipe_letter(wipe_letter(s, beg), end)
    return new


# Wipes "inside" letters (the middle ones)
def wipe_inner(s):
    """
    Removes the middle character(s) from the input string `s` and 
    then removes any occurrences of these characters from the resulting string.


    Args:
        s (str): The input string from which the middle character(s) will be removed.

    Returns:
        str: The new string with the middle character(s) removed.
    """
    quot, rem = divmod(len(s), 2)
    nb = 2 - rem
    if nb == 1:
        mid = s[quot]
        new = wipe_letter(s, mid)
    else:
        mid1 = s[quot - 1]
        mid2 = s[quot]
        new = wipe_letter(wipe_letter(s, mid1), mid2)
    return new


def wipe_along(name, wiper):
    """
    Repeatedly applies a wiper function to a normalized string until the result
    would be an empty string.

    Args:
        name (str): The input string to be processed.
        wiper (function): A function that takes a string and returns a modified string.

    Returns:
        str: The final string after the wiper function is fully applied.
    """
    old = str_norm(name)
    new = old
    while len(new) > 0:
        old = new
        new = wiper(old)
    return old


class GeneticProfile:

    def __init__(self, name):
        self.heart = wipe_along(name, wipe_outer)
        self.mantle = wipe_along(name, wipe_inner)
        self.genes = self.heart + self.mantle

        self._compute_gene_adv()
        self._compute_ranks()

    # Computes the genetic advantages, based on
    # the vowels of the "genes"
    def _compute_gene_adv(self):
        ld = {letter: 1 for letter in 'aeiouy'}
        for x in ld:
            ld[x] += self.genes.count(x) * 25 / 100
        self.gene_adv = ld

    # Computes the purity and nobility indices,
    # by averaging the "heart" and "mantle" respectively
    def _compute_ranks(self):
        
        def ratio(root):
            r = [ord(c) - ord('a') + 1 for c in root]
            return sum(r) / len(r)

        self.purity, self.nobility = ratio(self.heart), ratio(self.mantle)


    def get_components(self):
        return self.gene_adv, self.nobility, self.purity
