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
    norm_name = str_norm(name)

    ncut = []
    tmp = ''
    vow_cur = norm_name[0] in vow

    for i, letter in enumerate(norm_name):
        vow_now = letter in vow
        # two consecutive and different vowels can be grouped;
        # two consecutive consonants can also be grouped
        if vow_now == vow_cur:
            if len(tmp) == 2:
                ncut.append(tmp)
                tmp = ''
            elif letter in vow and tmp == letter:
                ncut.append(tmp)
                tmp = ''
            tmp += letter
        # a vowel followed by the nasal consonant 'n'
        # can be grouped with it
        elif letter == 'n' and (i + 1 == len(norm_name) or (norm_name[i + 1] in cons and norm_name[i + 1] != 'n')):
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
        occ = ud.get('occ', 0)
        occ += o
        ud['occ'] = occ
        its_list = ud.get('its', [])
        its_list += values
        ud['its'] = its_list
        dictionary[key] = ud

    l_init = lcut[0]
    d = {}
    k = ''
    v = []
    new_occ = False
    hanging = False
    for cut, label in zip(ncut, lcut):
        if label == 0:
            v.append(cut)
            if l_init > 0:
                upd_dict(d, k, v, 1 if new_occ else 0)
                v = []
                new_occ = False
                hanging = False
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
