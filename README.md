# Nomen Summon

Nomen Summon is a small Python program that allows you to generate the specs of a fantasy-like character. Details about the generation will be provided in the [end section](#how-it-works).

All the text displayed is written in French as it is my native language, but I might work on an English translation later.

Most of the written details used for the character descriptions (classes, species, inventory...) are personal choices. They can of course be altered on other branches to produce any kind of variation on this model of characters.

*This is just a small project I did to practice my base Python coding, so maybe you will not find it up to your expectations of optimized programming and well-written code. However I'm open to suggestions and willing to make this the best it can be!*

---

## Requirements
Apart from the standard Python 3 library, this package works with the following set of requirements (the versions are as I have them installed on my computer as of my last tests on the program):
- scipy (1.4.1)
- Unidecode (1.1.1)

## How to use it
Simply run the `main.py` file with Python on your command prompt. 

You will then be asked to type your **first name** (***prénom*** in French) and your **last name** (***nom de famille***).

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

### All execution options :

```
main.py -h | --help
main.py [-f <filename> [-a]] [<full_name> [...]],
  (a full_name has format <first_n> <last_n> )
main.py -c <ref_date> [<full_name> <date> [...]]
  (a date or ref_date has format 'YYYY-MM-DD' )
main.py -r <config_file>
```

#### Help
`main.py -h` and `main.py --help` will both display the execution options.


#### List of names (and `-f` option)
`main.py` followed by a sequence of names with format `first_name last_name` will result in the execution of the program for each of the full names given. Any improper use (i.e. missing last name or characters untranslatable to alphabet letters) will result in an error.

The `-f filename` option allows to write the results in a file, where `filename` designates the path. This option can be used without the list of names, the following behavior will be that of the general use (except the results will not be printed in the command line, but written in the file). 
- The additional option `-a` can be used to indicate that the results of the execution should be appended at the end of the file, and not written over the previous content.


#### Chaotic shift
`main.py -c ref_date` allows for a pseudo-random transformation of the names used during the process, based on the generation of a seed over which a transformation function is applied. This version of the program uses a difference of dates as the seed, then composed with a cosine curve. This allows for seemingly chaotic variations of the letters in the name (by preserving the vowel/consonant differences).

`ref_date` is the reference date, from which each given name must be distanced using a "birthdate" (or whatever date is preferrable). This can be used in a similar way to [the main option](#how-to-use-it) or [the list of names option](#list-of-names-and--f-option), except with the addition of a `date` to provide for each name.

At the moment, this option is not compatible with [file-writing](#list-of-names-and--f-option) or [configuration files](#reading-a-configuration-file), but it could be implemented shortly.


#### Reading a configuration file
`main.py -r config_file` allows to read configuration data, in the file `config_file`. The configuration file should be a text file, with the following conventions:

```
#   Every line starting with a hash is ignored in the section 
# prior to "start".
#   The results can be written in the file designated by 
# the path "filename". The string after "a" should be a boolean 
# indicating whether the new content must be appended to the 
# previous one on the file.
#
f filename
a True
#
#   After "start", the rest of the file is a list of names to be 
# compiled through the program. Names must be in the form 
# "First_name Last_name"; only one whitespace will be accounted 
# for, meaning composite first names or last names must be 
# written without spaces. No end character needs to be specified.
#   The results will be printed in the command line by default,
# or written in the specified file.
#
start
Jean Dupuis
Françoise Paulet
Dominique delaMothe
Jean-Marie Philippon
```

---

## How it works
The whole generation process is based on the sole information known about the character: their name.
I want to add more information in the future about the exact process, but it mostly works like this:
- the species is determined using the **first and last names**, with something one could call a *combinatory sum* (at least I do, there must be an actual term, which I have yet to find);
- clan data is derived from the **last name**, and affects abilities and inventory levels;
- abilities and inventory are both derived from the **first name**, respectively from groups of vowels and consonants in it.

I will also include some information about the chaotic shift process in the future.