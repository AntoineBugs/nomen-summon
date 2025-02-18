import pickle

# change this in order to import other variants
from data.variants.heroic_fantasy.data import (
    species_dict,
    items_dict,
    aptitudes,
    find_mastery_lvl,  # noqa: F401
    gen_classes,  # noqa: F401
)


#   Pickle dumping functions
# Use this script to regenerate pickle files
# Pickle files maintain default data versions


def species_dump():
    try:
        with open("species.pickle", "wb") as species_file:
            pickle.dump(species_dict, species_file)
    except IOError as e:
        print(f"An error occurred while writing to species.pickle: {e}")


def items_dump():
    try:
        with open("items.pickle", "wb") as items_file:
            pickle.dump(items_dict, items_file)
    except IOError as e:
        print(f"An error occurred while writing to items.pickle: {e}")


def apts_dump():
    try:
        with open("apts.pickle", "wb") as aptitudes_file:
            pickle.dump(aptitudes, aptitudes_file)
    except IOError as e:
        print(f"An error occurred while writing to apts.pickle: {e}")
