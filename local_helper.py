#!/bin/python3

"""
   Module with the helper functions for local modules of the package.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

"""

import typing
from itertools import product


def change_polarity(ngrams:list, alphabet:list, k:int) -> list:
    """ For a grammar with given polarity, returns set of ngrams
        of the opposite polarity.
    """

    combinations = set(generate_ngrams(alphabet, k))
    return list(combinations.difference(set(ngrams)))


def generate_ngrams(alphabet:list, k:int) -> list:
    """ Generate possible ngrams of a given length based on
        the given alphabet.
    """

    local_alphabet = alphabet[:]
    local_alphabet += [">", "<"]
    combinations = product(local_alphabet, repeat=k)
    ngrams = set([i for i in combinations if good_ngram(i)])
    return list(ngrams)


def good_ngram(ngram:tuple) -> bool:
    """ Auxiliary function for the tier sequence generator. Returns True
        iff the ngram is ill-formed, and False otherwise: if there is
        somthing in-between two start- or two end-symbols ('>a>'),
        something is before start symbol or after end symbol ('a>'), or
        if the ngram consists only of start- or only of end-symbols.
    """

    start = [i for i in range(len(ngram)) if ngram[i] == ">"]
    if len(start) > 0:
        s_inter = [i for i in range(start[0], start[-1]) if i not in start]
        if len(s_inter) > 0 or start[0] != 0 or len(start) == len(ngram):
            return False

    end = [i for i in range(len(ngram)) if ngram[i] == "<"]
    if len(end) > 0:
        e_inter = [i for i in range(end[0], end[-1]) if i not in end]
        if len(e_inter) > 0 or end[-1] != (len(ngram)-1) or len(end) == len(ngram):
            return False

    return True


def annotate_data(data:str, k:int) -> str:
    return ">"*(k-1) + data.strip() + "<"*(k-1)
