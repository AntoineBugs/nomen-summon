from unidecode import unidecode


def str_norm(s):
    """
    Normalize a string by converting it to lowercase, removing spaces and hyphens, 
    and converting accented characters to their unaccented counterparts.

    Args:
        s (str): The input string to be normalized.

    Returns:
        str: The normalized string.
    """
    us = s.lower().replace(" ", "").replace("-", "")
    return unidecode(us)


consonants = list("bcdfghjklmnpqrstvwxz")
vowels = list("aeiouy")


def cut_name(name):
    """
    Splits a given name into groups of letters based on vowel and consonant patterns.
    Args:
        name (str): The name to be split into groups.
    Returns:
        list: A list of strings, where each string is a group of letters from the name.
    """
    name2 = str_norm(name)

    ncut = []
    tmp = ""
    vow_cur = name2[0] in vowels

    for i, letter in enumerate(name2):
        vow_now = letter in vowels
        is_last_letter = i + 1 == len(name2)
        followed_by_cons = False
        if not is_last_letter:
            followed_by_cons = name2[i + 1] in consonants and name2[i + 1] != "n"
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
    """
    Handles the grouping of letters based on specific conditions, particularly focusing on the nasal consonant 'n'.

    Parameters:
    ncut (list): The list where the grouped letters are appended.
    tmp (str): The current temporary string being built.
    letter (str): The current letter being processed.
    vow_now (bool): A flag indicating if the current letter is a vowel.
    is_last_letter (bool): A flag indicating if the current letter is the last letter in the sequence.
    followed_by_cons (bool): A flag indicating if the current letter is followed by a consonant.

    Returns:
    tuple: A tuple containing the updated temporary string and the vowel status.
    """
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
    """
    Processes a letter to form groups of two letters and appends them to a list.

    Args:
        ncut (list): The list to which the two-letter groups are appended.
        tmp (str): The temporary string holding the current group of letters.
        letter (str): The current letter being processed.

    Returns:
        str: The updated temporary string after processing the current letter.
    """
    full_tmp = len(tmp) == 2
    vow_repeat = letter in vowels and tmp == letter
    if full_tmp or vow_repeat:
        ncut.append(tmp)
        tmp = ""
    tmp += letter
    return tmp


def label_cuts(ncut):
    """
    Assigns labels to each cut in the input list based on specific conditions.

    Parameters:
    ncut (list of str): A list of cuts to be labeled.

    Returns:
    list of int: A list of labels where:
        - 0 describes the consonant type.
        - 1 describes the vowel type.
        - 2 describes the nasal vowel type.
    """
    labels = []
    for c in ncut:
        if c[0] in consonants:
            x = 0
        elif c[-1] in vowels:
            x = 1
        else:
            x = 2
        labels.append(x)
    return labels


def group_cuts(ncut, lcut):
    """
    Groups cuts based on the provided labels and updates a dictionary with the grouped values.
    Args:
        ncut (list): A list of cuts.
        lcut (list): A list of labels corresponding to each cut in ncut.
    Returns:
        tuple: A tuple containing:
            - dictionary (dict): A dictionary where keys are group identifiers and values are lists of grouped cuts.
            - values (list): A list of remaining values that were not grouped.
    """
    l_init = lcut[0]
    dictionary, k, values = {}, "", []
    new_occ = False
    prev_cut = ""
    for cut, label in zip(ncut, lcut):
        k, values, new_occ = group_one_cut(
            l_init, dictionary, k, values, new_occ, prev_cut, cut, label
        )
        prev_cut = cut
    if k != "":  # leftover vowel group k
        upd_dict(dictionary, k, values, 1 if new_occ else 0)
    elif len(values) > 0:  # leftover consonant group v
        for x in dictionary:
            upd_dict(dictionary, x, values, 0, True)

    return dictionary, values


def group_one_cut(l_init, dictionary, k, values, new_occ, prev_cut, cut, label):
    """
    Processes a group of elements based on the provided label.

    Depending on the label, this function either processes a consonant group or a vowel group.
    For a consonant group (label == 0), it calls the `consonant_group` function.
    For a vowel group (label != 0), it calls the `vowel_group` function.

    Args:
        l_init (list): The initial list of elements to be processed.
        dictionary (dict): A dictionary used for processing.
        k (int): An integer parameter used in processing.
        values (list): A list of values to be updated.
        new_occ (int): An integer representing new occurrences.
        prev_cut (int): An integer representing the previous cut.
        cut (int): An integer representing the current cut.
        label (int): An integer label indicating the type of group (0 for consonant, non-zero for vowel).

    Returns:
        tuple: A tuple containing updated values of k, values, and new_occ.
    """
    hanging = False
    if label == 0:  # consonant group
        values, hanging = consonant_group(l_init, dictionary, k, values, new_occ, cut)
    else:  # vowel group
        k, values, new_occ = vowel_group(
            l_init, dictionary, k, values, prev_cut, cut, hanging
        )
    return k, values, new_occ


def vowel_group(l_init, dictionary, k, values, prev_cut, cut, hanging):
    """
    Processes a group of vowels and updates the dictionary accordingly.

    Args:
        l_init (int): The initial length or position of the vowel group.
        dictionary (dict): The dictionary to be updated with vowel group information.
        k (str): The current key or identifier for the vowel group.
        values (list): The list of values associated with the vowel group.
        prev_cut (str): The previous cut or delimiter used to separate groups.
        cut (str): The current cut or delimiter used to separate groups.
        hanging (bool): A flag indicating if the current vowel group is hanging (linked to the next group).

    Returns:
        tuple: A tuple containing the updated key (k), the updated list of values, and a boolean indicating if it's a new occurrence.
    """
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
    """
    Processes a consonant group and updates the dictionary with the given values.

    Args:
        l_init (int): Indicates if the consonant group is linked to a previous vowel group (non-zero) or not (zero).
        dictionary (dict): The dictionary to be updated.
        k (int): The key in the dictionary to be updated.
        values (list): The list of values to be updated.
        new_occ (bool): Indicates if this is a new occurrence.
        cut (any): The value to be appended to the values list.

    Returns:
        tuple: A tuple containing the updated values list and a boolean indicating if the group is hanging.
    """
    values.append(cut)
    if l_init > 0:  # linked to previous vowel group k
        upd_dict(dictionary, k, values, 1 if new_occ else 0)
        values = []
        new_occ = hanging = False
    else:  # linked to future vowel group, or all
        hanging = True
    return values, hanging


def upd_dict(dictionary, key, values, o, all=False, repeat=False):
    """
    Update a dictionary with the given key and values.

    Args:
        dictionary (dict): The dictionary to update.
        key (hashable): The key to update in the dictionary.
        values (list): The list of values to add to the 'its' list in the dictionary.
        o (int): The value to increment the 'occ' key by.
        all (bool, optional): A boolean value to append to the 'globals' list if repeat is False. Defaults to False.
        repeat (bool, optional): If False, append the 'all' value to the 'globals' list. Defaults to False.
    """
    ud = dictionary.get(key, {})
    ud["occ"] = ud.get("occ", 0) + o
    its_list = ud.get("its", [])
    ud["its"] = its_list + values
    globals = ud.get("globals", [])
    if not repeat:
        globals.append(all)
    ud["globals"] = globals
    dictionary[key] = ud
