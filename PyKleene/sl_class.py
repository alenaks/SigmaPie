#!/bin/python3

"""
   A class of Strictly Local Grammars.
   Copyright (C) 2018  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import warnings
from random import choice
from PyKleene.helper import *
from PyKleene.fsm import *
from PyKleene.grammar import *

class SL(L):
    """
    A class for strictly local grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar;
        fsm (FSM): finite state machine that corresponds to the grammar.

    Methods:
        learn: extracts strictly local grammar;
        annotate_string: appends to the string required number of
            start and end symbols;
        ngramize_data: returns a list of ngrams based on the given data;
        fsmize: create a FSM that corresponds to the given grammar;
        scan: scan the string and tell whether it's well-formed;
        generate_sample: generate data sample for the given SL grammar;
        switch_polarity: rewrites grammar to the opposite, and changes
            the polarity of the grammar;
        clean_grammar: removes useless ngrams from the grammar, i.e.
            the ones that cannot be used in any string of the language;
        extract_alphabet: extracts alphabet from data/grammar;
        well_formed_ngram: checks if ngram is well-formed;
        generate_all_ngrams: generates all possible well-formed ngrams
            based on the given alphabet;
        opposite_polarity: returns the opposite grammar;
        check_polarity: returns the polarity of the grammar;
        change_polarity: changes the polarity of the grammar to the one
            that is provided by the user.
    """

    def __init__(self, alphabet=None, grammar=None, k=2, data=None,
                 edges=[">", "<"], polar="p"):
        """ Initializes the PosSL object. """
        super().__init__(alphabet, grammar, k, data, edges, polar)
        self.fsm = FSM(initial=self.edges[0], final=self.edges[1])


    def learn(self):
        """ Extracts SL grammar from the given data. """
        if self.data:
            self.grammar = self.ngramize_data()
            if self.check_polarity() == "n":
                self.grammar = self.opposite_polarity(self.alphabet)

                
    def annotate_string(self, string):
        """ Annotates the string with the start and end symbols.

        Arguments:
            string (str): a string that needs to be annotated.

        Returns:
            str: annotated version of the string.
        """
        return ">"*(self.k-1) + string.strip() + "<"*(self.k-1)
        

    def ngramize_data(self):
        """
        Creates set of k-grams based on the given data.

        Returns:
            list: list of ngrams from the data.
        """
        if self.data == []:
            raise ValueError("The data is not provided.")

        ngrams = []
        for s in self.data:
            item = self.annotate_string(s)
            ngrams.extend(self.ngramize_item(item))

        return list(set(ngrams))


    def ngramize_item(self, item):
        """ This function n-gramizes a given string.

            Arguments:
                item (str): a string that needs to be ngramized.

            Returns:
                list: list of ngrams from the item.
        """
        ng = []
        for i in range(len(item)-(self.k-1)):
            ng.append(tuple(item[i:i+self.k]))

        return list(set(ng))


    def fsmize(self) -> None:
        """ Builds FSM corresponding to the given grammar and saves in
            it the fsm attribute.
        """
        if self.grammar:
            if self.check_polarity() == "p":
                self.fsm.sl_to_fsm(self.grammar)
            else:
                if self.alphabet:
                    opposite = self.opposite_polarity(self.alphabet)
                    self.fsm.sl_to_fsm(opposite)
                else:
                    raise ValueError("The alphabet is not provided.")
        else:
            raise(IndexError("The grammar is not provided."))


    def scan(self, string):
        """
        Checks whether the given string is well-formed with respect
        to the given grammar.

        Arguments:
            string (str): the string that needs to be evaluated.

        Returns:
            bool: tells whether the string is well-formed.
        """
        if not self.fsm.transitions:
            self.fsmize()
            
        string = self.annotate_string(string)
        return self.fsm.scan_sl(string)


    def generate_sample(self, n=10, rep=True, safe=True):
        """
        Generates a data sample of the required size, with or without
        repetitions.

        Arguments:
            n (int): the number of examples to be generated;
            rep (bool): allow (rep=True) or prohibit (rep=False)
               repetitions of the same data items;
            safe (bool): automatically break out of infinite looops,
                for example, when the grammar cannot generate the
                required number of data items, and the repetitions
                are set to False.

        Returns:
            list: generated data sample.
        """
        if not self.alphabet:
            raise ValueError("Alphabet cannot be empty.")
        if not self.fsm.transitions:
            raise ValueError("Corresponding fsm needs to be constructed.")

        statemap = self.state_map()
        data = [self.generate_item(statemap) for i in range(n)]

        if rep == False:
            data = set(data)
            warnings.warn("The grammar needs to be able to produce "
                          "the requested number of strings",
                          UserWarning)
            useless_loops = 0
            prev_len = len(data)
            while len(data) < n:
                data.add(self.generate_item(statemap))
                if prev_len == len(data): useless_loops += 1
                else: useless_loops = 0
                
                if safe == True and useless_loops > 100:
                    print("The grammar cannot produce the requested number"
                          " of strings.")
                    break

        return list(data)

                
    def generate_item(self, statemap):
        """
        Generates a well-formed string with respect to the given grammar.

        Arguments:
            statemap (dict): a dictionary of possible transitions
                in the corresponding fsm; constructed inside
                generate_sample.

        Returns:
            str: a well-formed string.
        """
        if any([len(statemap[x]) for x in statemap]) == 0:
            raise(ValueError("The grammar is not provided properly."))

        word = self.edges[0]*(self.k-1)
        while word[-1] != self.edges[1]:
            word += choice(statemap[word[-(self.k-1):]])
        return word[self.k-1:-1]


    def state_map(self):
        """ Generates a dictionary of possible transitions in
            the fsm corresponding to the grammar.

        Returns:
            the dictionary of the form
                {"previous_symbols":[list of possible next symbols]}.
        """
        local_alphabet = self.alphabet[:] + self.edges[:]
        poss = product(local_alphabet, repeat=self.k-1)
        
        smap = {}
        for i in poss:
            for j in self.fsm.transitions:
                if j[0] == i:
                    before = "".join(i)
                    if before in smap: smap[before] += j[1]
                    else: smap[before] = [j[1]]
        return smap


    def switch_polarity(self):
        """ Changes polarity of the grammar, and rewrites
            grammar to the opposite one.
        """
        if not self.alphabet:
            raise ValueError("Alphabet cannot be empty.")
        self.grammar = self.opposite_polarity(self.alphabet)
        self.change_polarity()


    def clean_grammar(self):
        """ Removes useless ngrams from the grammar.
            If negative, it just removes duplicates.
            If positive, it detects bigrams to which one cannot get
                from the initial symbol and from which one cannot get
                to the final symbol, and removes them.
        """
        if not self.fsm.transitions:
            self.fsmize()
            
        if self.check_polarity() == "n":
            self.grammar = list(set(self.grammar))
        elif self.check_polarity() == "p":
            self.fsm.trim_fsm()
            self.grammar = [j[0]+(j[1],) for j in self.fsm.transitions]
            
