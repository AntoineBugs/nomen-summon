import pickle

# change this in order to import other variants
from data.variants.heroic_fantasy.data import (
    species_dict,
    items_dict,
    aptitudes,
    find_mastery_lvl,  # noqa: F401
)


#   Pickle dumping functions
# You can use this script and its content to generate the pickle files again
# The pickle files can be used to maintain a default version of the data


def species_dump():
    with open("species.pickle", "wb") as species_file:
        pickle.dump(species_dict, species_file)


def items_dump():
    with open("items.pickle", "wb") as items_file:
        pickle.dump(items_dict, items_file)


def apts_dump():
    with open("apts.pickle", "wb") as aptitudes_file:
        pickle.dump(aptitudes, aptitudes_file)
