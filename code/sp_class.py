#!/bin/python3

"""
   A class of Strictly Piecewise Grammars.
   Copyright (C) 2019  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from random import choice
from itertools import product

from grammar import *
from fsm import *
from fsm_family import *
from helper import *

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
        scan(string): tells whether a given string is well-formed;
        learn(): extracts allowed or prohibited subsequences from
            the input data;
        subsequences(string): extracts subsequences of the length k from
            the input string;
        fsmize(): creates a corresponding FSM based on the
            training sample;
        generate_sample(n, repeat, safe): generates a sample of a given size;
        extract_alphabet(): extracts alphabet from data/grammar;
        generate_all_ngrams(): generates all possible well-formed ngrams
            based on the given alphabet;
        check_polarity(): returns the polarity of the grammar;
        switch_polarity(): changes the polarity of the grammar to the one
            that is provided by the user.
    """

    def __init__(self, alphabet=None, grammar=None, k=2, data=None, polar="p"):
        """ Initializes the SP object. """
        super().__init__(alphabet, grammar, k, data, polar=polar)
        self.fsm = FSMFamily()


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


    def fsmize(self):
        """
        Creates FSM family for the given SP grammar by passing every
        encountered subsequence through the corresponding automaton.
        """
        self.fsm = FSMFamily()

        if not self.grammar:
            self.learn()

        if self.check_polarity() == "p":
            data_subseq = self.grammar[:]
        else: data_subseq = self.opposite_polarity()

        # create a family of templates in fsm attribute
        seq = product(self.alphabet, repeat = self.k-1)
        for path in seq:
            f = FSM(initial=None, final=None)
            f.sp_build_template(path, self.alphabet, self.k)
            self.fsm.family.append(f)

        # run the input/grammar through the fsm family
        for f in self.fsm.family:
            for r in data_subseq:
                f.sp_fill_template(r)

        # clean the untouched transitions
        for f in self.fsm.family:
            f.sp_clean_template()


    def scan(self, string):
        """ Tells if the input string is well-formed.

        Arguments:
            string (str): string to be scanned.

        Returns:
            bool: True is well-formed, otherwise False.
        """

        subseq = self.subsequences(string)
        found_in_G = [(s in self.grammar) for s in subseq]
        
        if self.check_polarity == "p":
        	return all(found_in_G)
        else:
        	return not any(found_in_G)

        #if self.fsm == None:
        #    self.fsmize()

        #return self.fsm.run_all_fsm(string)


    def generate_item(self):
        """ Generates a well-formed string with respect
            to a given grammar.

        Returns:
            str: the generated string.
        """
        if not self.alphabet:
            raise ValueError("The alphabet must be provided.")

        string = ""
        while True:
            options = []
            for i in self.alphabet:
                if self.scan(string+i):
                    options.append(i)
            add = choice(options + ["EOS"])
            if add == "EOS": return string
            else: string += add


    def generate_sample(self, n=10, repeat=False, safe=True):
        """ Generates data sample of desired length.

        Arguments:
            n (int): the number of examples to be generated,
                the default value is 10;
            repeat (bool): allow (rep=True) or prohibit (rep=False)
               repetitions, the default value is False;
            safe (bool): automatically break out of infinite loops,
                for example, when the grammar cannot generate the
                required number of data items, and the repetitions
                are set to False.

        Returns:
            list: a list of generated examples.
        """
        
        sample = [self.generate_item() for i in range(n)]
        if repeat == False:
            useless_loops = 0
            sample = set(sample)
            prev_len = len(sample)
            while len(list(set(sample))) < n:
                sample.add(self.generate_item())
                if prev_len == len(sample): useless_loops += 1
                else: useless_loops = 0

                if safe == True and useless_loops > 100:
                    print("The grammar cannot produce the requested number"
                          " of strings.")
                    break

        return list(sample)


    def switch_polarity(self, new_polarity=None):
        """
        Changes the polarity of the grammar.

        Arguments:
            new_polarity ("p" or "n"): the new value of the polarity.
        """

        old_value = self.check_polarity()
        self.change_polarity(new_polarity)
        new_value = self.check_polarity()

        if old_value != new_value:
        	self.grammar = self.opposite_polarity()