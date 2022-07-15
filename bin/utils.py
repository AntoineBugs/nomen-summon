from unidecode import unidecode


# String normalization
def str_norm(s):
    us = s.lower().replace(' ', '').replace('-', '')
    return unidecode(us)


cons = list('bcdfghjklmnpqrstvwxz')
vow = list('aeiouy')


# Cuts the name in one or two-letters parts,
# separating vowels from consonants (to the exception
# of the nasal consonant 'n')
def cut_name(name):
    name2 = str_norm(name)

    ncut = []
    tmp = ''
    vow_cur = name2[0] in vow

    for i, letter in enumerate(name2):
        vow_now = letter in vow
        is_last_letter = i + 1 == len(name2)
        followed_by_cons = False
        if not is_last_letter:
            followed_by_cons = name2[i + 1] in cons and name2[i + 1] != 'n'
        # general case: a group consists of two letters,
        # either two consonants or two different vowels
        if vow_now == vow_cur:
            full_tmp = len(tmp) == 2
            vow_repeat = letter in vow and tmp == letter
            if full_tmp or vow_repeat:
                ncut.append(tmp)
                tmp = ''
            tmp += letter
        # special case: the nasal consonant 'n'
        # can also be grouped with a vowel group
        elif letter == 'n' and (is_last_letter or followed_by_cons):
            tmp += letter
            ncut.append(tmp)
            vow_cur = vow_now
            tmp = ''
        # for any other case, the cut is systematic
        else:
            vow_cur = vow_now
            ncut.append(tmp)
            tmp = letter
    if tmp != '':
        ncut.append(tmp)

    return ncut


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
    # updates an occurrence dict d
    # by adding occurrences o
    # and items v
    def upd_dict(dictionary, key, values, o):
        ud = dictionary.get(key, {})
        ud['occ'] = ud.get('occ', 0) + o
        its_list = ud.get('its', [])
        its_list += values
        ud['its'] = its_list
        dictionary[key] = ud

    l_init = lcut[0]
    d, k, v = {}, '', []
    new_occ = hanging = False
    for cut, label in zip(ncut, lcut):
        if label == 0:
            v.append(cut)
            if l_init > 0:
                upd_dict(d, k, v, 1 if new_occ else 0)
                v = []
                new_occ = hanging = False
            else:
                hanging = True
        else:
            if hanging and l_init > 0:
                upd_dict(d, k, v, 1)
                v = []
            k = cut
            if l_init == 0:
                upd_dict(d, k, v, 1)
                k = ''
                v = []
                hanging = False
            else:
                hanging = True
            new_occ = True
    if k != '':
        upd_dict(d, k, v, 1 if new_occ else 0)
    elif len(v) > 0:
        for x in d:
            upd_dict(d, x, v, 0)

    return d
