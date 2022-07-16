# Nomen Summon

Nomen Summon is a small Python program that allows you to generate the specs of a fantasy-like character.

All the text displayed is written in French as it is my native language, but I might work on an English translation later.

*This is just a small project I did to practice my base Python coding, so maybe you will not find it up to your expectations of optimized programming and well-written code. However I'm open to suggestions and willing to make this the best it can be!*

---

## Dependencies
Apart from the standard Python 3 library, this package works with the following set of dependencies (the versions are as I have them installed on my computer as of my last tests on the program):
- scipy (1.4.1)
- Unidecode (1.1.1)

## How to use it
Simply execute the `main.py` file on your command prompt. 

You will then be asked to type your **first name** (***prénom*** in French) and your **last name** (***nom de famille*** in French).

The program will then print your "character sheet", with in order:
1. the full name, species and level of your character;
2. a description of their species;
3. some data about their clan: 
  - genetic advantages;
  - a nobility and a purity index;
4. the list of their abilities (classes and powers), detailing:
  - the level of mastery;
  - the description of the ability;
  - the pieces of inventory used by your character in conjunction with this ability;
  - other pieces of inventory used in conjuction with all abilities.

### More execution options :

```bash
main.py [-h|--help]
main.py <-f filename <-a>> <first_n last_n>
```

---

## How it works
The whole generation process is based on the sole information known about the character: their name.
I will add some more details in the future about the exact process, but it mostly works like this:
- the species is determined using the **first and last names**, with something one (me at least) might call a *combinatory sum* (there must be an actual term for this, but I have yet to find it);
- clan data is derived from the **last name**, and affects abilities and inventory levels;
- abilities and inventory are both derived from the **first name**.
