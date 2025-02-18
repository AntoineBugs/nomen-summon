from math import cos, lcm
from datetime import datetime, date


def date_diff(ref: date, y: int, m: int, d: int):
    """
    Calculate the difference in days between a reference date and a given date.

    Args:
        ref (date): The reference date.
        y (int): Year of the given date.
        m (int): Month of the given date.
        d (int): Day of the given date.

    Returns:
        int: The difference in days.
    """
    dt = datetime(y, m, d)
    diff = dt.date() - ref
    return diff.days


def shift_float(f, ref: date):
    return lambda y, m, d: f(date_diff(ref, y, m, d))


def cos_shift(ref: date):
    """
    Applies a cosine shift transformation to a given reference date.
    This function creates a cosine-based transformation function and applies
    it to the provided reference date using the `shift_float` function.
    Args:
        ref (date): The reference date to which the cosine shift transformation
                    will be applied.
    Returns:
        function: A function that takes a single argument `x` and returns the
                  transformed value using the cosine shift formula.
    """
    def f(x):
        return (cos(x) + 1) / 2

    return shift_float(f, ref)


def interval_conversion(x, f_min, f_max, i_min, i_max):
    """
    Converts a value from one interval to another.

    Parameters:
    x (float): The value to be converted.
    f_min (float): The minimum value of the original interval.
    f_max (float): The maximum value of the original interval.
    i_min (float): The minimum value of the target interval.
    i_max (float): The maximum value of the target interval.

    Returns:
    float: The value converted to the target interval.
    """
    x_frac = (x - f_min) / (f_max - f_min)
    return x_frac * (i_max - i_min) + i_min


def cos_to_interval(x, i_min, i_max):
    """
    Converts a cosine value to a specified interval.

    Args:
        x (float): The cosine value to be converted, expected to be in the range [0, 1].
        i_min (float): The minimum value of the target interval.
        i_max (float): The maximum value of the target interval.

    Returns:
        float: The value converted to the specified interval [i_min, i_max].
    """
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
    """
    Change the letters in the input string based on a shift value and a range.
    Args:
        shift (float): The shift value used to determine the seed for letter changes.
        fmin: The minimum value of the range for the shift.
        fmax: The maximum value of the range for the shift.
        vowels (str): A string containing all the vowels to be considered.
        string (str): The input string whose letters are to be changed.
    Returns:
        str: The modified string with letters changed based on the shift value.
    """
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
    """
    Transforms a list of characters into new words based on a seed value and specified rules.

    Args:
        vowels (list): A list of vowel characters.
        consonants (list): A list of consonant characters.
        size (int): The size parameter used for modulus operations.
        lens (list): A list of integers representing the lengths of the new words.
        chars (list): A list of characters to be transformed.
        seed (int): A seed value used to determine the transformation.

    Returns:
        list: A list of new words formed by transforming the input characters.
    """
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
    """
    Shifts a character by a specified number of positions within a given string.

    Args:
        char (str): The character to be shifted.
        letter_shift (int): The number of positions to shift the character.
        among (str): The string within which the character is shifted.

    Returns:
        str: The character after being shifted within the given string.

    Raises:
        ValueError: If the character is not found in the given string.
    """
    ind = among.index(char)
    ind = (ind + letter_shift) % len(among)
    return among[ind]
