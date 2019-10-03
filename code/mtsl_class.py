#!/bin/python3

"""
   A class of Multiple Tier-based Strictly Local Grammars.
   Copyright (C) 2019  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from copy import deepcopy
from random import choice, randint
from itertools import product
from tsl_class import *


class MTSL(TSL):
    """
    A class for tier-based strictly local grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar.
 
    Methods:
        learn: extracts tier-based strictly local grammar;
        annotate_string(string): adds start and end symbols to the 
            given string;
        ngramize_data: returns a list of ngrams used in the given data;
        scan(string): scan the string and tell whether it's well-formed;
        extract_alphabet: extracts alphabet from data/grammar;
        generate_all_ngrams(alphabet, k): generates all `k`-long ngrams
            based on the given `alphabet`;
        opposite_polarity(alphabet): returns the opposite grammar for 
            the given `alphabet` and the locality of the grammar;
        check_polarity: returns the polarity of the grammar;
        switch_polarity: rewrites grammar to the opposite, and changes
            the polarity of the grammar;
        change_polarity(new_polarity): changes the polarity of the 
            grammar either to `new_polarity` if one is given, or to
            the opposite than before (does not change the grammar).

    NOT IMPLEMENTED (requires more theoretical work):
        learn for k > 2;
        fsmize;
        generate_sample;
        clean_grammar.
    """
    
    def __init__(self, alphabet=None, grammar=None, k=2, data=None,
                 edges=[">", "<"], polar="p"):
        """ Initializes the TSL object. """
        super().__init__(alphabet, grammar, k, data, edges, polar)
        if self.k != 2:
        	raise NotImplementedError("The learner for k-MTSL languages is "
        							  "still being designed.")


    def learn(self):
        """
        Learns 2-local MTSL grammar for a given sample. The algorithm 
        currently works only for k=2 and is based on MTSL2IA designed 
        by McMullin, Aksenova and De Santo (2019). We are currently
        working on lifting the locality of the grammar to arbitrary k.

        Results:
            self.grammar is updated with a grammar of the following shape:
            {(tier_1):[bigrams_for_tier_1],
                ...
             (tier_n):[bigrams_for_tier_n]}
        """
        if not self.data:
    	    raise ValueError("Data needs to be provided.")
        if not self.alphabet:
    	    raise ValueError("The alphabet is empty. Provide data or "
    	    	"run `grammar.extract_alphabet`.")

        possible = set(self.generate_all_ngrams(self.alphabet, self.k))
        attested = set()
        for d in self.data:
            bigrams = self.ngramize_item(self.annotate_string(d))
            attested.update(set(bigrams))
        unattested = list(possible.difference(attested))

        paths = self.all_paths(self.data)
        grammar = []

        for bgr in unattested:
            tier = self.alphabet[:]

            for s in self.alphabet:
                rmv = True

                # condition 1
                if s in bgr:
                    rmv = False
                    continue

                # condition 2
                relevant_paths = []
                for p in paths:
                    if (p[0] == bgr[0]) and (p[-1] == bgr[-1]) and (s in p[1]):
                        relevant_paths.append(p)
                for rp in relevant_paths:
                    new = [rp[0], [i for i in rp[1] if i != s], rp[2]]
                    if new not in paths:
                        rmv = False
                        break

                # remove from the tier if passed both conditions
                if rmv:
                    tier.remove(s)

            grammar.append((tier, bgr))
        gathered = self.gather_grammars(grammar)

        self.grammar = gathered
        if self.check_polarity() == "p":
            self.grammar = self.opposite_polarity()


    def scan(self, string):
        """
        Scan string with respect to a given MTSL grammar.

        Arguments:
            string (str): a string that needs to be scanned.

        Returns:
            bool: well-formedness of the string.
        """
        tier_evals = []

        for tier in self.grammar:
            t = tier
            g = self.grammar[tier]

            delete_non_tier = "".join([i for i in string if i in t])
            tier_image = self.annotate_string(delete_non_tier)
            ngrams = self.ngramize_item((tier_image))

            this_tier = [(ngr in g) for ngr in ngrams]

            if self.check_polarity() == "p":
                tier_evals.append(all(this_tier))
            else:
                tier_evals.append(not any(this_tier))

        return all(tier_evals)


    def gather_grammars(self, grammar):
        """
        Gathers grammars with the same tier together.

        Arguments:
            grammar (list): a representation of the learned grammar
                where there is a one-to-one mapping between tiers 
                and bigrams.

        Returns:
            dict: a dictionary where keys are tiers and values are
                the restrictions imposed on those tiers.
        """
        G = {}
        for i in grammar:
            if tuple(i[0]) in G:
                G[tuple(i[0])] += [i[1]]
            else:
                G[tuple(i[0])] = [i[1]]
        return G


    def path(self, string):
        """
        Collects a list of paths from a string. A path is a 
        triplet <a, X, b>, where `a` is a symbol, `b` is a symbol
        that follows `a` in `string`, and `X` is a set of symbols 
        in-between `a` and `b`.

        Arguments:
            string (str): a string paths of which need to be found.

        Returns:
            list: list of paths of `string`.
        """
        string = self.annotate_string(string)
        paths = []

        for i in range(len(string) - 1):
            for j in range(i + 1, len(string)):
                path = [string[i]]
                path.append(list(set([k for k in string[(i + 1):j]])))
                path.append(string[j])

                if path not in paths:
                    paths.append(path)

        return paths


    def all_paths(self, dataset):
        """
        Finds all paths that are present in a list of strings.

        Arguments:
            dataset (list): a list of strings.

        Returns:
            list: a list of paths present in `dataset`.
        """
        paths = []
        for item in dataset:
            for p in self.path(item):
                if p not in paths:
                    paths.append(p)

        return paths


    def opposite_polarity(self):
        """
        Generates a grammar of the opposite polarity.

        Returns:
            dict: a dictionary containing the opposite ngram lists
                for every tier of the grammar.
        """
        if not self.grammar:
            raise ValueError("Grammar needs to be provided. It can also "
                             "be learned using `grammar.learn()`.")
        opposite = {}
        for i in self.grammar:
            possib = self.generate_all_ngrams(list(i), self.k)
            opposite[i] = [j for j in possib if j not in self.grammar[i]]

        return opposite


    def switch_polarity(self):
        """ Changes polarity of the grammar, and rewrites
            grammar to the opposite one.
        """
        self.grammar = self.opposite_polarity()
        self.change_polarity()


    def clean_grammar(self, **kwargs):
        raise NotImplementedError("Requires theoretical work.")

    def fsmize(self, **kwargs):
        raise NotImplementedError("Requires theoretical work.")

    def generate_sample(self, **kwargs):
        raise NotImplementedError("Requires theoretical work.")
