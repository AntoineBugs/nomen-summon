from scipy.special import comb

from bin.data_access import species_dict as species

from bin.utils import str_norm


# Computes and return the combinatorial sum for a given name.
def compute_name(name):
    letter_ranks = [ord(c) - ord('a') + 1 for c in str_norm(name)]
    intervals = len(letter_ranks) - 1
    res = 0
    for k, x in enumerate(letter_ranks):
        res += x * comb(intervals, k)
    return res


class SpeciesProfile:

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
