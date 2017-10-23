#!/bin/python3

"""
   Module with general helper functions for the subregular package.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

"""

from typing import Tuple


def alphabetize(data:list) -> list:
    """ Collects alphabets from the list of data. """

    alphabet = set()
    for item in data:
        alphabet.update({i for i in item})
    return sorted(list(alphabet))


def get_gram_info(ngrams:list) -> Tuple[list, int]:
    """ Detects the alphabet and window size of the grammar """

    alphabet = list(set([i for i in "".join(ngrams) if i not in [">", "<"]]))       
    k = max(len(i) for i in ngrams)
    return alphabet, k

