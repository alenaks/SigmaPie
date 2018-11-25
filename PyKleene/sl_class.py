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
        polar ("p" or "n"): polarity of the grammar.
        fsm (FSM): finite state machine that corresponds to the grammar.

    Methods:
        extract_alphabet: extracts alphabet from data/grammar;
        well_formed_ngram: checks if ngram is well-formed;
        generate_all_ngrams: generates all possible well-formed ngrams
            based on the given alphabet;
        opposite_polarity: changes the polarity of the grammar to the opposite,
            and returns the opposite grammar;
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




####################################################################
##
##
##    def generate_sample(self, n:int=10, rep:bool=True) -> None:
##        """
##        Generates a sample of the data of a given size.
##
##        Arguments:
##        -- self;
##        -- n (optional): the number of examples, the default value is 10;
##        -- rep (optional): allow (rep=True) or prohibit (rep=False)
##               repetitions, the default value is True.
##
##        Results:
##        -- self.data_sample is being generated.
##
##        """
##        
##        self.fsmize()
##        self.extract_alphabet()
##
##        data = [self.generate_item() for i in range(n)]
##        self.data_sample = data
##
##        if rep == False:
##            self.data_sample = list(set(self.data_sample))
##            while len(self.data_sample) < n:
##                self.data_sample += [self.generate_item()]
##                self.data_sample = list(set(self.data_sample))
##
##
##    def scan(self, string:str) -> bool:
##        """
##        Checks whether the given string can be generated by the grammar.
##
##        Arguments:
##        -- self;
##        -- string: the string that needs to be evaluated.
##
##        Returns:
##        -- a boolean value depending on the well-formedness of the string
##           with respect to the given grammar.
##        """
##        
##        if not self.grammar:
##            self.learn()
##
##        string = self.annotate_data(string, self.k)
##        if set(self.ngramize_item(string, self.k)).issubset(set(self.grammar)):
##            return True
##        else:
##            return False
##
##
##    def clean(self) -> None:
##        """
##        Removes useless n-grams from the grammar. Useless ngrams are
##        that can never be used in the language.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- self.fsm contains the FSM of the current grammar;
##        -- self.grammar is being cleaned.
##        """
##
##        self.fsmize()
##        self.fsm.trim_fsm()
##        self.grammar = self.build_ngrams(self.fsm.transitions)
##
##
##    def change_polarity(self) -> None:
##        """
##        Changes polarity of the grammar.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- self.grammar is being switched to the opposite;
##        -- self.__class__ is changed to 'NegSL'.
##        """
##
##        if not self.alphabet:
##            self.extract_alphabet()
##        self.grammar = self.opposite_polarity(self.grammar, self.alphabet, self.k)
##        self.__class__ = NegSL
##
##
##    def generate_item(self) -> str:
##        """
##        Generates a well-formed sequence of symbols.
##
##        Arguments:
##        -- self.
##
##        Returns:
##        -- a well-formed sequence with respect to a given grammar.
##        """
##        
##        smap = self.state_map()
##        if any([len(smap[x]) for x in smap]) == 0:
##            raise(ValueError("The grammar is not provided properly."))
##
##        word = self.edges[0]*(self.k-1)
##        while word[-1] != self.edges[1]:
##            word += choice(smap[word[-(self.k-1):]])
##        word += self.edges[1]*(self.k-2)
##
##        return word
##
##
##    def state_map(self) -> dict:
##        """ Generates a dictionary of possible transitions in the given FSM.
##
##        Arguments:
##        -- self.
##
##        Returns:
##        -- the dictionary of the form
##            {"previous_symbols":[list of possible next symbols]}.
##        """
##            
##        smap:dict = {}
##        local_alphabet = self.alphabet[:] + self.edges[:]
##        poss = product(local_alphabet, repeat=self.k-1)
##        for i in poss:
##            for j in self.fsm.transitions:
##                if j[0] == i:
##                    before = "".join(i)
##                    if before in smap:
##                        smap[before] += j[1]
##                    else:
##                        smap[before] = [j[1]]
##        return smap
##
##        

##
