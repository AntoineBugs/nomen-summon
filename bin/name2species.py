from scipy.special import comb

from data.data import species_dict as species

from bin.utils import str_norm


def compute_name(name):
    """
    Computes a numerical value for a given name based on the ranks of its letters.

    The function normalizes the input name, converts each letter to its corresponding rank 
    (where 'a' is 1, 'b' is 2, ..., 'z' is 26), and then calculates a weighted sum of these ranks 
    using binomial coefficients.

    Args:
        name (str): The input name to be computed.

    Returns:
        int: The computed numerical value of the name.
    """
    letter_ranks = [ord(c) - ord("a") + 1 for c in str_norm(name)]
    intervals = len(letter_ranks) - 1
    res = 0
    comb_cache = {}
    for k, x in enumerate(letter_ranks):
        if (intervals, k) not in comb_cache:
            comb_cache[(intervals, k)] = comb(intervals, k)
        res += x * comb_cache[(intervals, k)]
    return res


class SpeciesProfile:
    """
    A class to represent a species profile.
    Attributes
    ----------
    species : str
        The name of the species.
    desc : str
        The description of the species.
    Methods
    -------
    __init__(firstN, familyN):
        Initializes the SpeciesProfile with a species name and description based on the provided first and family names.
    """
    def __init__(self, firstN, familyN):
        fir = compute_name(firstN)
        fam = compute_name(familyN)

        # computing the species index
        num = (fir + fam) % len(species.keys())
        spec = species[num]

        # species name
        self.species = spec[0]
        # species description
        self.desc = spec[1]
