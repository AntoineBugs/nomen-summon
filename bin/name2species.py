from scipy.special import comb
import pickle
from .utils import str_norm

# species is an ordered list of tuples,
# of the form ("species name","species description")
with open('bin/species.pickle','rb') as file:
	species = pickle.load(file)

# Computes and return the combinatory sum for a given name.
def compute_name(name):
	l = [ord(c) - ord('a') + 1 for c in str_norm(name)]
	N = len(l)-1
	res = 0
	for k,x in enumerate(l):
		res += x*comb(N,k)
	return res

class SpeciesProfile():

	def __init__(self,firstN,familyN):
		fir = compute_name(firstN)
		fam = compute_name(familyN)

		# computing the species index
		num = (fir + fam) % 26
		spec = species[num]
		
		# species name
		self.species = spec[0]
		# species description
		self.desc = spec[1]