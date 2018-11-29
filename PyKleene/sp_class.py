#!/bin/python3

"""
   A class of Strictly Piecewise Grammars.
   Copyright (C) 2018  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from random import choice
from itertools import product
from PyKleene.grammar import *
from PyKleene.fsm import *
#from PyKleene.fsm_family import *
from PyKleene.helper import *

class SP(L):
    """
    A class for strictly piecewise grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar;
        fsm (FSM): finite state machine that corresponds to the grammar.

    Methods:
        MORE METHODS
        subsequences: extracts subsequences of the length k from
            the input string;
        extract_alphabet: extracts alphabet from data/grammar;
        well_formed_ngram: checks if ngram is well-formed;
        generate_all_ngrams: generates all possible well-formed ngrams
            based on the given alphabet;
        opposite_polarity: returns the opposite grammar;
        check_polarity: returns the polarity of the grammar;
        change_polarity: changes the polarity of the grammar to the one
            that is provided by the user.
    """

    def __init__(self, alphabet=None, grammar=None, k=2, data=None, polar="p"):
        """ Initializes the SP object. """
        super().__init__(alphabet, grammar, k, data)
        self.__polarity = polar
        self.fsm = FSM(initial=None, final=None)


    def subsequences(self, string):
        """ Extracts k-long subsequences out of the given word.

        Arguments:
            string (str): a string that needs to be processed.

        Returns:
            list: a list of subsequences out of the string.
        """
        if len(string) < self.k:
            return []
        
        start = list(string[:self.k])
        result = [start]

        previous_state = [start]
        current_state = []

        for s in string[self.k:]:
            for p in previous_state:
                for i in range(self.k):
                    new = p[:i] + p[i+1:] + [s]
                    current_state.append(new)
            result.extend(current_state)
            previous_state = current_state[:]
            current_state = []
            
        return list(set([tuple(i) for i in result]))


    def learn(self):
        """
        Learns possible subsequences of the given length.

        Arguments:
        -- self.

        Results:
        -- self.grammar is updated.
        """

        if not self.data:
            raise ValueError("The data must be provided.")
        if not self.alphabet:
            raise ValueError("The alphabet must be provided.")
        
        self.grammar = []

        for i in self.data:
            for j in self.subsequences(i):
                if j not in self.grammar:
                    self.grammar.append(j)

        if self.check_polarity() == "n":
            self.grammar = self.opposite_polarity()


    def opposite_polarity(self):
        """ Returns the grammar opposite to the current one. """
        all_ngrams = product(self.alphabet, repeat = self.k)
        return [i for i in all_ngrams if i not in self.grammar]

                    

    
#####################################################################
##

##
##
##    def fsmize(self:PosStP) -> None:
##        """
##        Creates FSM family for the given SP grammar.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- fills self.fsm with the corresponding FSMFamily object.
##        """
##
##        self.fsm = FSMFamily()
##
##        if not self.grammar:
##            self.learn()
##
##        seq = self.generate_paths(self.k-1)
##        for i in seq:
##            f = FiniteStateMachine()
##            f.sp_template(i, self.alphabet, self.k)
##            self.fsm.family.append(f)
##
##        for f in self.fsm.family:
##            for d in self.grammar:
##                f.run_learn_sp(d)
##
##        for f in self.fsm.family:
##            f.sp_clean()
##
##
##    def generate_sample(self:PosStP, n:int=10, rep:bool=False) -> None:
##        """
##        Generates a sample of the data of a given size.
##
##        Arguments:
##        -- self;
##        -- n (optional): the number of examples, the default value is 10;
##        -- rep (optional): allow (rep=True) or prohibit (rep=False)
##               repetitions, the default value is False.
##
##        Results:
##        -- self.data_sample is being generated.
##        """
##        
##        sample = []
##        for i in range(n):
##            sample.append(self.generate_item())
##
##        if rep == False:
##            while len(list(set(sample))) < n:
##                sample.append(self.generate_item())
##
##        self.data_sample = list(set(sample))
##
##
##    def scan(self:PosStP, w:str) -> None:
##        """
##        Accepts of rejects the given string.
##
##        Arguments:
##        -- self;
##        -- w: string to be checked.
##
##        Returns:
##        -- boolean depending on well-formedness of the string.
##        """
##        
##        if self.fsm == None:
##            self.fsmize()
##
##        return self.fsm.run_all(w)
##
##
##    def change_polarity(self:PosStP) -> None:
##        """
##        Changes polarity of the grammar.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- self.grammar is being switched to the opposite;
##        -- self.__class__ is changed to 'NegSP'.
##        """
##
##        if not self.alphabet:
##            self.extract_alphabet()
##        self.grammar = self.opposite_polarity()
##        self.__class__ = NegSP
##
##
##    def generate_item(self:PosStP) -> None:
##        """
##        Generates an item well-formed with respect to
##        a given grammar.
##
##        Arguments:
##        -- self.
##
##        Returns:
##        -- a well-formed string of a language.
##        """
##
##        if not self.alphabet:
##            self.extract_alphabet()
##
##        string = ""
##        while True:
##            options = []
##            for i in self.alphabet:
##                if self.scan(string+i):
##                    options.append(i)
##            add = choice(options + ["EOS"])
##            if add == "EOS":
##                return string
##            else:
##                string += add
##            
##    
##    def generate_paths(self:PosStP, rep:int) -> None:
##        """
##        Generates all possible permutations of the alphabet items
##        of the desired length.
##
##        Arguments:
##        -- self;
##        -- rep: length of the generated sequences.
##
##        Returns:
##        -- the list of generated sequences.
##        
##        """
##        
##        return product(self.alphabet, repeat=rep)
##
##
##
##
##
##    def opposite_polarity(self:PosStP) -> list:
##        """
##        For a grammar with given polarity, returns set of ngrams
##        of the opposite polarity.
##
##        Arguments:
##        -- self.
##
##        Returns:
##        -- a list of ngrams opposite to the ones given as input.
##        """
##
##        opposite = []
##        possib = self.generate_paths(self.k)
##        for i in possib:
##            if i not in self.grammar:
##                opposite.append(i)
##                
##        return opposite
##
##
##
##class NegSP(PosSP):
##    """ A class for negative strictly piecewise grammars.
##
##    Attributes:
##    -- alphabet: the list of symbols used in the given language;
##    -- grammar: the list of grammatical rules;
##    -- k: the locality measure;
##    -- data: the language data given as input;
##    -- data_sample: the generated data sample;
##    -- fsm: the finite state machine that corresponds to the given grammar.
##    """
##
##    def learn(self:NegStP) -> None:
##        """
##        Learns possible subsequences of the given length.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- self.grammar is updated.
##        """
##
##        if self.data:
##            self.extract_alphabet()
##            
##        super().learn()
##        self.grammar = self.opposite_polarity()
##
##
##    def fsmize(self:PosStP) -> None:
##        """
##        Creates FSM family for the given SP grammar.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- fills self.fsm with the corresponding FSMFamily object.
##        """
##
##        self.grammar = self.opposite_polarity()
##        super().fsmize()
##        self.grammar = self.opposite_polarity()
##
##
##    def change_polarity(self:NegStP) -> None:
##        """
##        Changes polarity of the grammar.
##
##        Arguments:
##        -- self.
##
##        Results:
##        -- self.grammar is being switched to the opposite;
##        -- self.__class__ is changed to 'PosSP'.
##        """
##
##        if not self.alphabet:
##            self.extract_alphabet()
##        self.grammar = self.opposite_polarity()
##        self.__class__ = NegSP
##
