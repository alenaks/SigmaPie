"""Module with general helper functions for the subregular package. Copyright
(C) 2019  Alena Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""


def alphabetize(data):
    """Detects symbols used in the input data.

    Arguments:
        data (list): Input data.
    Returns:
        list:  Symbols used in these examples.
    """
    alphabet = set()
    for item in data:
        alphabet.update({i for i in item})
    return sorted(list(alphabet))


def get_gram_info(ngrams):
    """Returns the alphabet and window size of the grammar.

    Arguments:
        ngrams (list): list of ngrams.
    Returns:
        (list, int)
            list: alphabet;
            int: locality window.
    """
    alphabet = list(set([i for i in "".join(ngrams) if i not in [">", "<"]]))
    k = max(len(i) for i in ngrams)
    return alphabet, k


def prefix(w):
    """Returns a list of prefixes of a given string.

    Arguments:
        w (str): a string prefixes of which need to be extracted.
    Returns:
        list: a list of prefixes of the given string.
    """
    return [w[:i] for i in range(len(w) + 1)]


def lcp(*string):
    """
    Finds the longest common prefix of an unbounded number of strings.
    Arguments:
        *string (str): one or more strings;
    Returns:
        str: a longest common prefix of the input strings.
    """
    w = list(set(i for i in string if i != "*"))
    if not w:
        raise IndexError("At least one non-unknown string needs to be provided.")

    result = ""
    n = min([len(x) for x in w])
    for i in range(n):
        if len(set(x[i] for x in w)) == 1:
            result += w[0][i]
        else:
            break

    return result


def remove_from_prefix(w, pref):
    """Removes a substring from the prefix position of another string.

    Arguments:
        w (str): a string that needs to be modified;
        pref (str): a prefix that needs to be removed from the string.
    Returns:
        str: the modified string.
    """
    if w.startswith(pref):
        return w[len(pref) :]
    elif w == "*":
        return w

    raise ValueError(pref + " is not a prefix of " + w)
