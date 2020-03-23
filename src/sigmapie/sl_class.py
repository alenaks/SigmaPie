"""A class of Strictly Local Grammars. Copyright (C) 2019  Alena Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

from random import choice
from sigmapie.helper import *
from sigmapie.fsm import *
from sigmapie.grammar import *


class SL(L):
    """A class for strictly local grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): collection of ngrams;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar;
        fsm (FSM): corresponding finite state machine.
    """

    def __init__(
        self, alphabet=None, grammar=None, k=2, data=None, edges=[">", "<"], polar="p"
    ):
        """Initializes the SL object."""
        super().__init__(alphabet, grammar, k, data, edges, polar)
        self.fsm = FSM(initial=self.edges[0], final=self.edges[1])

    def learn(self):
        """Extracts SL grammar from the given data."""
        self.grammar = self.ngramize_data()
        if self.check_polarity() == "n":
            self.grammar = self.opposite_polarity(self.alphabet)

    def annotate_string(self, string):
        """Annotates the string with the start and end symbols.

        Arguments:
            string (str): a string that needs to be annotated.
        Returns:
            str: annotated version of the string.
        """
        return ">" * (self.k - 1) + string.strip() + "<" * (self.k - 1)

    def ngramize_data(self):
        """Creates set of n-grams based on the given data.

        Returns:
            list: collection of ngrams in the data.
        """
        if not self.data:
            raise ValueError("The data is not provided.")

        ngrams = []
        for s in self.data:
            item = self.annotate_string(s)
            ngrams.extend(self.ngramize_item(item))

        return list(set(ngrams))

    def ngramize_item(self, item):
        """This function n-gramizes a given string.

        Arguments:
            item (str): a string that needs to be ngramized.
        Returns:
            list: list of ngrams from the item.
        """
        ng = []
        for i in range(len(item) - (self.k - 1)):
            ng.append(tuple(item[i : (i + self.k)]))

        return list(set(ng))

    def fsmize(self):
        """Builds FSM corresponding to the given grammar and saves it in the
        fsm attribute."""
        if not self.grammar:
            raise (IndexError("The grammar must not be empty."))
        if not self.alphabet:
            raise ValueError(
                "The alphabet is not provided. " "Use `grammar.extract_alphabet()`."
            )

        if self.check_polarity() == "p":
            self.fsm.sl_to_fsm(self.grammar)
        else:
            opposite = self.opposite_polarity(self.alphabet)
            self.fsm.sl_to_fsm(opposite)

    def scan(self, string):
        """Checks if the given string is well-formed with respect to the given
        grammar.

        Arguments:
            string (str): the string that needs to be evaluated.
        Returns:
            bool: well-formedness value of a string.
        """
        if not self.fsm.transitions:
            self.fsmize()

        string = self.annotate_string(string)
        return self.fsm.scan_sl(string)

    def generate_sample(self, n=10, repeat=True, safe=True):
        """Generates a data sample of the required size, with or without
        repetitions depending on `repeat` value.

        Arguments:
            n (int): the number of examples to be generated;
            repeat (bool): allows (rep=True) or prohibits (rep=False)
               repetitions within the list of generated items;
            safe (bool): automatically breaks out of infinite loops,
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
        if not any([len(statemap[x]) for x in statemap]):
            raise (
                ValueError(
                    "There are ngrams in the grammar that are"
                    " not leading anywhere. Clean the grammar "
                    " or run `grammar.clean_grammar()`."
                )
            )

        data = [self.generate_item(statemap) for i in range(n)]

        if not repeat:
            data = set(data)
            useless_loops = 0
            prev_len = len(data)

            while len(data) < n:
                data.add(self.generate_item(statemap))

                if prev_len == len(data):
                    useless_loops += 1
                else:
                    useless_loops = 0

                if safe and useless_loops > 500:
                    print(
                        "The grammar cannot produce the requested "
                        "number of strings. Check the grammar, "
                        "reduce the number, or allow repetitions."
                    )
                    break

        return list(data)

    def generate_item(self, statemap):
        """Generates a well-formed string with respect to the given grammar.

        Arguments:
            statemap (dict): a dictionary of possible transitions in the
                corresponding fsm; constructed inside generate_sample.
        Returns:
            str: a well-formed string.
        """
        word = self.edges[0] * (self.k - 1)
        while word[-1] != self.edges[1]:
            word += choice(statemap[word[-(self.k - 1) :]])
        return word[(self.k - 1) : -1]

    def state_map(self):
        """
        Generates a dictionary of possible transitions in the FSM.
        Returns:
            dict: the dictionary of the form
                {"keys":[list of possible next symbols]}, where 
                keys are (k-1)-long strings.
        """
        local_alphabet = self.alphabet[:] + self.edges[:]
        poss = product(local_alphabet, repeat=(self.k - 1))

        smap = {}
        for i in poss:
            for j in self.fsm.transitions:
                if j[0] == i:
                    before = "".join(i)
                    if before in smap:
                        smap[before] += j[1]
                    else:
                        smap[before] = [j[1]]
        return smap

    def switch_polarity(self):
        """Changes polarity of the grammar, and changes the grammar to the
        opposite one."""
        if not self.alphabet:
            raise ValueError("Alphabet cannot be empty.")

        self.grammar = self.opposite_polarity(self.alphabet)
        self.change_polarity()

    def clean_grammar(self):
        """Removes useless ngrams from the grammar.

        If negative, it just removes duplicates. If positive, it detects
        bigrams to which one cannot get     from the initial symbol and
        from which one cannot get     to the final symbol, and removes
        them.
        """
        if not self.fsm.transitions:
            self.fsmize()

        if self.check_polarity() == "n":
            self.grammar = list(set(self.grammar))
        else:
            self.fsm.trim_fsm()
            self.grammar = [j[0] + (j[1],) for j in self.fsm.transitions]
