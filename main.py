import bin.name2species as nts
import bin.name2clan as ntc
from bin.utils import str_norm, cut_name, label_cuts, group_cuts
from math import floor
import pickle

class Character():

	def __init__(self,firstN,familyN):
		self.firstN = firstN
		self.familyN = familyN
		self.species = nts.SpeciesProfile(self.firstN,self.familyN)
		self.clan = ntc.GeneticProfile(self.familyN)
		self.compute_apts()

	# computes the aptitudes, their levels and inventories
	def compute_apts(self):
		ncut = cut_name(self.firstN)
		sizes = [len(cut) for cut in ncut]
		self.tot_size = sum(sizes)
		lcut = label_cuts(ncut)
		self.pow_size = sum([size if label < 2 else 0 for (size,label) in zip(sizes,lcut)])
		self.groups = group_cuts(ncut,lcut)
		self.extract_apts()

	# computes the aptitude levels
	def extract_apts(self):
		
		with open('bin/items.pickle','rb') as file:
			items = pickle.load(file)
		with open('bin/apts.pickle','rb') as file:
			apts = pickle.load(file)
		
		advs = self.clan.gene_adv
		nobility = self.clan.nobility
		purity = self.clan.purity

		tot_skills_lvl = 0
		tot_added_vals = 0
		
		skillset = []
		
		for group,assoc in self.groups.items():
			its = assoc['its']
			occ = assoc['occ']

			skill = {}

			src = apts['classes'] if group[-1] != 'n' else apts['powers']
			key = ''.join(sorted(group)) if group[-1] != 'n' else ''.join(sorted(group[:-1]))+'n'
			apt = src[key]
			skill['name'] = apt['name']
			skill['desc'] = apt['desc']
			
			size = occ * len(key)
			# base level
			lvl = 100 * size / self.pow_size
			# items added value
			valits = self.extract_items(its,items)
			itadd = sum([it[1] for it in valits])
			# genetic advantage
			adv = self.key2adv(key,advs)	
			# advanced level
			skill['level'] = floor(adv * (itadd + lvl))

			tot_skills_lvl += skill['level']
			tot_added_vals += itadd

			inventory = []
			for it,valit in zip(its,valits):
				spec = {}
				spec['name'] = valit[0]
				spec['type'] = valit[2]
				if valit[2] != 'inclassable':
					coef = 53 - (nobility if valit[2] == 'objet' else purity)
					coef /= 26
					size = len(it)
					spec['level'] = floor(100 * coef * size / self.pow_size)
				inventory.append(spec)

			skill['items'] = inventory

			skillset.append(skill)

		self.skills = skillset

		skill_part = tot_skills_lvl / 100
		skill_part += 1

		remainder = 100 * (self.tot_size - self.pow_size) / self.pow_size
		remainder += 100 + tot_added_vals

		self.level = floor(skill_part*remainder)
	
	# computes the item levels
	def extract_items(self,its,items):
		
		def findkey(it,src):
			l = [k if it in k else '' for k in src.keys()]
			return ''.join(l)

		def findcompkey(it,items):

			def rev(l):
				nl = l.copy()
				nl.reverse()
				return nl

			simple = items['simple']
			comp = items['composed']
			k = [findkey(c,simple) for c in it]
			if k[0] == k[1]:
				key = k[0]
				composed = False
			else:
				key = findkey('+'.join(k),comp) + findkey('+'.join(rev(k)),comp)
				composed = True
			
			return key,composed
		
		val = []
		for it in its:
			if len(it) == 1:
				src = items['simple']
				key = findkey(it,src)
				val.append(src[key])
			else:
				key,composed = findcompkey(it,items)
				if composed:
					src = items['composed']
					val.append(src[key])
				else:
					src = items['simple']
					(n,v,t) = src[key]
					val.append((n,2*v,t))
		return val
	

	def key2adv(self,key,advs):
		adv = 1
		for c in key:
			if c != 'n':
				adv *= advs[c]
		return adv
    
# Prompts the first and last names and computes the Character object
def make_char():
	err_msg = "Votre entrée ne peut contenir que des lettres (accents permis), des espaces et des traits d'union."

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
	return Character(prenom,nom)


# Builds a string for an aptitude 
def skill2str(skill):
	name = skill['name']
	desc = skill['desc']
	lvl = skill['level']
	its = skill['items']

	s = "· {} niveau {}\n".format(name.capitalize(),lvl)
	s += '\t' + desc + '\n'
	if len(its) > 0:
		s += "\tInventaire :"
		for it in its:
			if it['type'] != "inclassable":
				s += "\n\t· {} niveau {}".format(it['name'].capitalize(),it['level'])
			else:
				s += "\n\t· {}".format(it['name'].capitalize())

	return s

# Prints a Character object
def print_char(ch):
	fir = ch.firstN#
	fam = ch.familyN#
	lvl = ch.level#

	sp = ch.species#
	sp_n = sp.species#
	sp_d = sp.desc#
	
	clan = ch.clan#
	cl_a = clan.gene_adv#
	l = []
	for k,v in cl_a.items():
		if v > 1:
			l.append(k)
	adv = []
	if len(l)<1:
		adv.append("aucun")
	else:
		if 'a' in l:
			adv.append("la magie")
		if 'e' in l:
			adv.append("l'archerie")
		if 'i' in l:
			adv.append("l'escrime")
		if 'o' in l:
			adv.append("la lutte")
		if 'u' in l:
			adv.append("l'acrobatie")
		if 'y' in l:
			adv.append("la science")
	cl_n = clan.nobility#
	cl_p = clan.purity#
	
	sk = ch.skills

	header = "*** {} {} - {} niveau {} ***".format(fir,fam,sp_n.capitalize(),lvl)
	body_spec = "Description de l'espèce :\n\t{}".format(sp.desc)

	body_clan = "Détails du clan :\n"
	gadv = ', '.join(adv)
	body_clan += "\tAvantages génétiques " + ("pour " if len(l)>0 else ": ") + gadv + ".\n"
	body_clan += "\tNoblesse de lignée : {}\n".format(cl_n)
	body_clan += "\tPureté de lignée : {}\n".format(cl_p)
	body_clan += "~ Les indices de noblesse et de pureté sont situés entre 1 (pureté ou noblesse maximale) et 26 (pureté ou noblesse minimale) ~\n"
	
	body_skills = "Aptitudes et pouvoirs :\n"
	for a in sk:
		body_skills += skill2str(a) + '\n'

	s = '\n'.join([header,body_spec,body_clan,body_skills])
	# len_max = max(len(l) for l in s.splitlines())
	# bar = len_max*'-' + '\n'
	# print(bar + s + bar)
	print(s)



#### EXECUTION ####

ch = make_char()
print()
print_char(ch)