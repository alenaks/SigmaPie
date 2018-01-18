#!/bin/python3

"""
   A class of Tier-based Strictly Local Grammars.
   Copyright (C) 2017  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from typing import TypeVar, Generator, Union
from sl_class import *

PTSL = TypeVar('PTSL', bound='PosTSL')

class PosTSL(PosSL):
    """ A class for positive strictly local grammars.

    Attributes:
    -- alphabet: the list of symbols used in the given language;
    -- grammar: the list of grammatical rules;
    -- k: the locality measure;
    -- data: the language data given as input;
    -- data_sample: the generated data sample;
    -- fsm: the finite state machine that corresponds to the given grammar;
    -- tier: the list of tier symbols.
    
    """
    
    def __init__(self:PTSL, alphabet:Union[None,list]=None, grammar:Union[None,List[tuple]]=None, k:int=2,
                 data:Union[list,None]=None, edges=[">", "<"], tier:Union[None,list]=None) -> None:
        """ Initializes the PosTSL object. """
        
        super().__init__(alphabet, grammar, k, data, edges)
        self.tier = tier


    def learn(self:TSL) -> None:
        pass




"""

    def learn(self:TSL) -> None:
    Function for extracting negative SL grammar and alphabet
            from the given data.
 
        if self.data:
            self.alphabet = alphabetize(self.data)
        else:
            raise IndexError("Language is not provided or empty -- "
                             "no grammar can be generated.")
        self.tier = self.alphabet[:]

        ngrams = self._ngramize_data(self.k, self.data)
        ngrams_less = self._ngramize_data(self.k-1, self.data)
        ngrams_more = self._ngramize_data(self.k+1, self.data)
        
        for symb in self.tier:
            if self.__run_tests(symb, ngrams, ngrams_less):
                print(symb, "must be deleted")

    def __run_tests(self:TSL, symb:str, ngrams:list, ngrams_less:list) -> bool:
     Runs tests to determine whether a symbol is a tier symbol 

        test_ins = list(self.__test_insert(symb, ngrams, ngrams_less))
        if all(test_ins) == True:
            return True
        else:
            return False
        
    def __test_insert(self:TSL, symb:str, ngrams:list, ngrams_less:list) -> Generator[bool, None, None]:
  
        
        for ngram in ngrams_less:
            new:list = []
            for ind in range(len(ngram)+1):
                copy = list(ngram)
                copy.insert(ind, symb)
                if good_ngram(tuple(copy)):
                    new.append(tuple(copy))
            if set(new).issubset(set(ngrams)):
                yield True
            else:
                yield False

    def __test_remove(self:TSL, symb:str, ngrams:list, ngrams_less:list) -> Generator[bool, None, None]:
        
        
        pass
        




        ngrams = ngramize_all(obj, n, param)

        # for every symbol in tier, check whether the two tests hold
        for symb in sigma:
            if test_insert(obj, n, param, symb, ngrams) and test_remove(obj, n, param, symb, ngrams):
                # if they do, check whether removing this symbol from the tier will
                # produce tier sequences that were not found in the input data
                if erase_test(obj, tier, param, ngrams, symb, n):
                    # if no, remove the symbol from the tier
                    tier.remove(symb)

        # generate all possible tier ngrams
        possib = generate_ngrams(tier, n)

        # extract from the set of possible ngrams those that are allowed
        # construct the negative tsl grammar
        neg_gram = possib.difference(ngrams)

        # if the requested grammar is positive, change its polarity
        if positive == True:
            pos_gram = change_polarity(neg_gram, tier, n)
            return pos_gram

        # if negative grammar is expected, return it without modifications              
        return neg_gram

        

    def erase(data, tier, param):
         Removes non-tier symbols from the data 

        for item in data:
            parsed = preprocess(item, param)
            tier_image = []

            # collects only tier items of the input data
            for i in parsed:
                if i in tier:
                    tier_image.append(i)

            # reassembles the data, and yields it
            yield "".join(tier_image)
                    


    def erase_test(data, tier, param, ngrams, symb, n):
         Erasing test: checks that removing the symb from the list
            of tier symbols will not predict ngrams that were not found
            in the initial data.
        
        
        newtier = [i for i in tier if i != symb]
        
        # create a tier image of the input data, and ngramize it
        newdata = erase(data, newtier, param)
        new_ngrams = ngramize_all(newdata, n, param)
        
        return new_ngrams.issubset(ngrams)



    def test_insert(obj, n, param, symb, ngrams):
         Insertion test: check that for in every (n-1)-gram of the
            original text it is possible to insert the symbols under
            consideration in it. If not, it is a tier symbol.
        

        # get the list of (n-1)-grams
        test = ngramize_all(obj, n-1, param)
        
        # deal with the special case where "<" and ">" are lost
        if (n-1) == 1:
            test.add((">",))
            test.add(("<",))

        # if a symbol can be inserted anywhere, it might be not
        # a tier symbol, depends on the second test
        answer = True
        for i in test:
            a = set(gen_insert(i, symb))
            if not (a.issubset(ngrams)):
                answer = False
                
        return answer


    def gen_insert(ngram, symb):
        Auxiliary function for the insertion test 
        
        # define start as 0 or index after the last ">"
        # define end as the last index or index after the first "<"
        start = 0
        end = len(ngram)+1
        if ">" in ngram:
            ind = [x for x in range(len(ngram)) if ngram[x] == ">"]
            start = ind[-1]+1
        if "<" in ngram:
            ind = [x for x in range(len(ngram)) if ngram[x] == "<"]
            end = ind[0] + 1

        # generate possible sequences where the symbol is inserted
        # in the ngram
        for i in range(start, end):
            yield ngram[:i] + (symb,) + ngram[i:]



    def test_remove(obj, n, param, symb, ngrams):
        Deleteion test: check that for all (n+1)-grams containint
            the symbol under consideration, this symbol can be removed
            from there. If not, it is a tier symbol.
        

        # get the list of (n+1)-grams containing the needed symbol
        t = ngramize_all(obj, n+1, param)
        test = set([i for i in t if (symb in i) and (i[n-1] != ">") \
                    and (i[-n] != "<")])

        # if a symbol can be removed from anywhere, it might be not
        # a tier symbol, depends on the first test
        answer = True
        for i in test:
            a = set(gen_remove(i, symb))
            if not (a.issubset(ngrams)):
                answer = False
                
        return answer


    def gen_remove(ngram, symb):
        Auxiliary function for the deletion test

        # generate a set of sequences where each instance of the symbol
        # is removed from the ngram
        for i in range(len(ngram)):
            if ngram[i] == symb:
                yield ngram[:i] + ngram[i+1:]
"""
