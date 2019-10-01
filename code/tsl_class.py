#!/bin/python3

"""
   A class of Tier-based Strictly Local Grammars.
   Copyright (C) 2019  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from random import choice, randint
from sl_class import *


class TSL(SL):
    """
    A class for tier-based strictly local grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar;
        fsm (FSM): finite state machine that corresponds to the grammar;
        tier (list): list of tier symbols.
 
i   Methods:
        learn: extracts tier and tier-based strictly local grammar;
        learn_tier: extracts the list of tier symbols;
        tier_image: returns tier image of the given string;
        annotate_string: appends to the string required number of
            start and end symbols;
        ngramize_data: returns a list of ngrams based on the given data;
        fsmize: create a FSM that corresponds to the given grammar;
        scan: scan the string and tell whether it's well-formed;
        generate_sample: generate data sample for the given SL grammar;
        switch_polarity: rewrites grammar to the opposite, and changes
            the polarity of the grammar;
        extract_alphabet: extracts alphabet from data/grammar;
        well_formed_ngram: checks if ngram is well-formed;
        generate_all_ngrams: generates all possible well-formed ngrams
            based on the given alphabet;
        opposite_polarity: returns the opposite grammar;
        check_polarity: returns the polarity of the grammar.
    """
    
    def __init__(self, alphabet=None, grammar=None, k=2, data=None,
                 edges=[">", "<"], polar="p", tier=None):
        """ Initializes the TSL object. """
        
        super().__init__(alphabet, grammar, k, data, edges, polar)
        self.tier = tier
        self.fsm = FSM(initial=self.edges[0], final=self.edges[1])


    def learn(self):
        """ Updates grammar attribute based on the given data. """

        if not self.alphabet:
            raise ValueError("Alphabet cannot be empty.")
        if not self.data:
            raise ValueError("Data needs to be provided.")

        self.learn_tier()
        tier_sequences = [self.tier_image(i) for i in self.data]
        self.grammar = TSL(k=self.k, data=tier_sequences).ngramize_data()

        if self.check_polarity() == "n":
            self.grammar = self.opposite_polarity(self.tier)
            

    def learn_tier(self) -> None:
        """
        This function determines which of the symbols used in
        the language are tier symbols, algorithm by Jardine &
        McMullin (2017). Updates tier attribute.
        """
        self.tier = self.alphabet[:]

        ngrams = self.ngramize_data()
        ngrams_less = TSL(data=self.data, k=self.k-1).ngramize_data()
        ngrams_more = TSL(data=self.data, k=self.k+1).ngramize_data()

        for symbol in self.tier:
            if self.test_insert(symbol, ngrams, ngrams_less) and \
               self.test_remove(symbol, ngrams, ngrams_more):
                self.tier.remove(symbol)


    def test_insert(self, symbol, ngrams, ngrams_less):
        """ 
        Tier presense test #1. For every (n-1)-gram ('x','y','z'),
        there must be n-grams of the type ('x','S','y','z') and
        ('x','y','S','z').

        Arguments:
            symbol (str): the symbol that is currently being tested;
            ngrams (list): the list of n-gramized input;
            ngrams_less (list): the list of (n-1)-gramized input.
            
        Returns:
            bool: True if a symbol passed the test, otherwise False.
        """
        extension = []
        for small in ngrams_less:
            for i in range(len(small)):
                new = small[:i] + (symbol,) + small[i:]
                if self.well_formed_ngram(new):
                    extension.append(new)
                    
        if set(extension).issubset(set(ngrams)): return True
        else: return False


    def test_remove(self, symbol, ngrams, ngrams_more):
        """
        Tier presense test #2. For every (n+1)-gram of the type ('x','S','y'),
        there must be an n-gram of the type ('x', 'y').

        Arguments:
            symbol (str): the symbol that is currently being tested;
            ngrams (list): the list of n-gramized input;
            ngrams_more (list): the list of (n+1)-gramized input.
            
        Returns:
            bool: True if a symbol passed the test, otherwise False.
        """
        extension = []
        for big in ngrams_more:
            if symbol in big:
                for i in range(len(big)):
                    if big[i] == symbol:
                        new = big[:i] + big[i+1:]
                        if self.well_formed_ngram(new):
                            extension.append(new)

        if set(extension).issubset(set(ngrams)): return True
        else: return False


    def tier_image(self, string):
        """
        Function that returns a tier image of the input string.

        Arguments:
            string (str): string tier image of which needs to
                be obtained.
        
        Returns:
            str: tier image of the input string.
        """
        new = ""
        for i in string:
            if i in self.tier:
                new += i
        return new


    def fsmize(self):
        """ Builds FSM corresponding to the given grammar and saves in
            it the fsm attribute.
        """
        if self.grammar:
            if self.check_polarity() == "p":
                self.fsm.sl_to_fsm(self.grammar)
            else:
                if self.tier:
                    opposite = self.opposite_polarity(self.tier)
                    self.fsm.sl_to_fsm(opposite)
                else:
                    raise ValueError("The tier is not learned yet,"
                                     " or the tier is empty.")
        else:
            raise(IndexError("The grammar is not provided."))


    def switch_polarity(self):
        """ Changes polarity of the grammar, and rewrites
            grammar to the opposite one.
        """
        if not self.tier:
            raise ValueError("Either the language is SL, or"
                             " tier is not extracted yet.")
        self.grammar = self.opposite_polarity(self.tier)
        self.change_polarity()
        

    def generate_sample(self, n=10, repeat=True, safe=True):
        """
        Generates a data sample of the required size, with or without
        repetitions.

        Arguments:
            n (int): the number of examples to be generated;
            repeat (bool): allow (rep=True) or prohibit (rep=False)
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
            self.fsmize()

        statemap = self.state_map()
        data = [self.generate_item() for i in range(n)]

        if repeat == False:
            data = set(data)
            useless_loops = 0
            prev_len = len(data)
            while len(data) < n:
                data.add(self.generate_item())
                if prev_len == len(data): useless_loops += 1
                else: useless_loops = 0
                
                if safe == True and useless_loops > 100:
                    print("The grammar cannot produce the requested number"
                          " of strings.")
                    break

        return list(data)


    def generate_item(self):
        """
        Generates a well-formed sequence of symbols.

        Returns:
            str: a well-formed string.
        """
        if not self.fsm.transitions:
            self.fsmize()

        tier_seq = self.annotate_string(super().generate_item(self.state_map()))
        ind = [x for x in range(len(tier_seq)) if tier_seq[x] not in self.edges]
        if not ind:
            tier_items = []
        else:
            tier_items = list(tier_seq[ind[0]:(ind[-1]+1)])
        free_symb = list(set(self.alphabet).difference(set(self.tier)))
        
        new_string = self.edges[0]*(self.k-1)
        for i in range(self.k+1):
            if randint(0,1) == 1:
                new_string += choice(free_symb)

        if tier_items:
            for item in tier_items:
                new_string += item
                for i in range(self.k+1):
                    if randint(0,1) == 1:
                        new_string += choice(free_symb)

        new_string = "".join([i for i in new_string if i not in self.edges])
       
        return new_string


    def state_map(self):
        """
        Generates a dictionary of possible transitions in the given FSM.
 
        Returns:
            dict: dictionary of the form
                {"previous_symbols":[list of possible next symbols]}.
        """

        if self.fsm is None:
            self.fsmize()
            
        smap = {}
        local_alphabet = self.tier[:] + self.edges[:]
        poss = product(local_alphabet, repeat=self.k-1)
        for i in poss:
            for j in self.fsm.transitions:
                if j[0] == i:
                    before = "".join(i)
                    if before in smap:
                        smap[before] += j[1]
                    else:
                        smap[before] = [j[1]]
        return smap



    def scan(self, string):
        """
        Function that checks if the given string can be generated by the grammar.

        Arguments:
            string (str): the string that needs to be evaluated.

        Returns:
	        bool: True if the string is well-formed, otherwise False.
        """
        tier_img = self.annotate_string(self.tier_image(string))
        matches = [(n in self.grammar) for n in self.ngramize_item(tier_img)]
        if self.check_polarity() == "p":
        	return all(matches)
        else:
        	return not any(matches)