from unidecode import unidecode


# String normalization
def str_norm(s):
    us = s.lower().replace(" ", "").replace("-", "")
    return unidecode(us)


cons = list("bcdfghjklmnpqrstvwxz")
vow = list("aeiouy")


# Cuts the name in one or two-letters parts,
# separating vowels from consonants (to the exception
# of the nasal consonant 'n')
def cut_name(name):
    name2 = str_norm(name)

    ncut = []
    tmp = ""
    vow_cur = name2[0] in vow

    for i, letter in enumerate(name2):
        vow_now = letter in vow
        is_last_letter = i + 1 == len(name2)
        followed_by_cons = False
        if not is_last_letter:
            followed_by_cons = name2[i + 1] in cons and name2[i + 1] != "n"
        if vow_now == vow_cur:
            # general case: a group consists of two letters,
            # either two consonants or two different vowels
            tmp = two_letters_group(ncut, tmp, letter)
        else:
            tmp, vow_cur = other_group(
                ncut, tmp, letter, vow_now, is_last_letter, followed_by_cons
            )
    if tmp != "":
        ncut.append(tmp)
    return ncut


def other_group(ncut, tmp, letter, vow_now, is_last_letter, followed_by_cons):
    # special case: the nasal consonant 'n'
    # can also be grouped with a vowel group
    if letter == "n" and (is_last_letter or followed_by_cons):
        tmp += letter
        ncut.append(tmp)
        vow_cur = vow_now
        tmp = ""
    # for any other case, the cut is systematic
    else:
        vow_cur = vow_now
        ncut.append(tmp)
        tmp = letter
    return tmp, vow_cur


def two_letters_group(ncut, tmp, letter):
    full_tmp = len(tmp) == 2
    vow_repeat = letter in vow and tmp == letter
    if full_tmp or vow_repeat:
        ncut.append(tmp)
        tmp = ""
    tmp += letter
    return tmp


# Labels each cut : 0 for consonants,
# 1 for vowels, 2 for nasal vowels
def label_cuts(ncut):
    labels = []
    for c in ncut:
        if c[0] in cons:
            x = 0
        elif c[-1] in vow:
            x = 1
        else:
            x = 2
        labels.append(x)
    return labels


# Groups consonants with their respective vowels
def group_cuts(ncut, lcut):
    l_init = lcut[0]
    dictionary, k, values = {}, "", []
    new_occ = False
    prev_cut = ""
    for cut, label in zip(ncut, lcut):
        k, values, new_occ = group_one_cut(
            l_init, dictionary, k, values, new_occ, prev_cut, cut, label
        )
    if k != "":  # leftover vowel group k
        upd_dict(dictionary, k, values, 1 if new_occ else 0)
    elif len(values) > 0:  # leftover consonant group v
        for x in dictionary:
            upd_dict(dictionary, x, values, 0, True)

    return dictionary, values


def group_one_cut(l_init, dictionary, k, values, new_occ, prev_cut, cut, label):
    if label == 0:  # consonant group
        values, hanging = consonant_group(l_init, dictionary, k, values, new_occ, cut)
    else:  # vowel group
        k, values, new_occ = vowel_group(
            l_init, dictionary, k, values, prev_cut, cut, hanging
        )
    prev_cut = cut
    return k, values, new_occ


def vowel_group(l_init, dictionary, k, values, prev_cut, cut, hanging):
    if hanging and l_init > 0:  # hanging linked to last vowel group k
        upd_dict(dictionary, k, values, 1)
        values = []
    repeat = prev_cut == cut
    k = cut
    if l_init == 0:  # linked to previous consonant group v
        upd_dict(dictionary, k, values, 1, repeat=repeat)
        k = ""
        values = []
        hanging = False
    else:  # linked to future consonant group
        hanging = True
    new_occ = True
    return k, values, new_occ


def consonant_group(l_init, dictionary, k, values, new_occ, cut):
    values.append(cut)
    if l_init > 0:  # linked to previous vowel group k
        upd_dict(dictionary, k, values, 1 if new_occ else 0)
        values = []
        new_occ = hanging = False
    else:  # linked to future vowel group, or all
        hanging = True
    return values, hanging


# updates an occurrence dict dictionary
# by adding occurrences o
# and items values
# with characteristic 'all' to values
def upd_dict(dictionary, key, values, o, all=False, repeat=False):
    ud = dictionary.get(key, {})
    ud["occ"] = ud.get("occ", 0) + o
    its_list = ud.get("its", [])
    ud["its"] = its_list + values
    globals = ud.get("globals", [])
    if not repeat:
        globals.append(all)
    ud["globals"] = globals
    dictionary[key] = ud
