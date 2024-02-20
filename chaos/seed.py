from math import cos, lcm
from datetime import datetime, date


def date_diff(ref: date, y: int, m: int, d: int):
    dt = datetime(y, m, d)
    diff = dt.date() - ref
    return diff.days


def shift_float(f, ref: date):
    return lambda y, m, d: f(date_diff(ref, y, m, d))


def cos_shift(ref: date):
    def f(x):
        return (cos(x) + 1) / 2

    return shift_float(f, ref)


def interval_conversion(x, f_min, f_max, i_min, i_max):
    x_frac = (x - f_min) / (f_max - f_min)
    return x_frac * (i_max - i_min) + i_min


def cos_to_interval(x, i_min, i_max):
    return interval_conversion(x, 0, 1, i_min, i_max)


# def get_functions(ref):
#     d = {"date_diff": lambda y, m, d: date_diff(ref, y, m, d)}
#     d.update({"shift_float": lambda f: shift_float(f, ref)})
#     d.update({"sin_shift": cos_shift(ref)})
#     d.update(
#         {
#             "sin_to_interval": lambda i_min, i_max: cos_to_interval(
#                 cos_shift(ref), i_min, i_max
#             )
#         }
#     )
#     return d


def change_letters(shift: float, fmin, fmax, vowels: str, string: str):
    def get_consonants(vowels):
        alpha = [chr(ord("a") + i) for i in range(26)]
        for v in vowels:
            alpha.remove(v)
        return "".join(alpha)

    consonants = get_consonants(vowels)
    size = lcm(len(vowels), 26 - len(vowels))
    words = string.lower().split()
    lens = [len(w) for w in words]
    chars = "".join(words)
    extent = size ** len(chars)
    seed = int(interval_conversion(shift, fmin, fmax, 0, extent - 1))
    new_words = change_words(vowels, consonants, size, lens, chars, seed)
    return " ".join(new_words)


def change_words(vowels, consonants, size, lens, chars, seed):
    new_words = [[]]
    cur_w = 0
    past_w = 0
    for i in range(len(chars)):
        is_vowel = vowels.count(chars[i])
        modulus = len(vowels) if is_vowel else 26 - len(vowels)
        digit = seed % size
        letter_shift = digit % modulus
        seed //= size
        among = vowels if is_vowel else consonants
        new_char = shift_char(chars[i], letter_shift, among)
        if i - past_w >= lens[cur_w]:
            past_w += lens[cur_w]
            cur_w += 1
            new_words.append([])
        new_words[cur_w].append(new_char)
    new_words = ["".join(w) for w in new_words]
    return new_words


def shift_char(char: str, letter_shift: int, among: str):
    ind = among.index(char)
    ind = (ind + letter_shift) % len(among)
    return among[ind]
