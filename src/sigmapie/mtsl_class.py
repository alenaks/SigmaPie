"""A class of Multiple Tier-based Strictly Local Grammars. Copyright (C) 2019
Alena Aksenova.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.
"""

from copy import deepcopy
from random import choice, randint
from itertools import product
from sigmapie.tsl_class import *
from sigmapie.fsm_family import *


class MTSL(TSL):
    """A class for tier-based strictly local grammars and languages.

    Attributes:
        alphabet (list): alphabet used in the language;
        grammar (list): the list of substructures;
        k (int): locality window;
        data (list): input data;
        edges (list): start- and end-symbols for the grammar;
        polar ("p" or "n"): polarity of the grammar;
        fsm (FSMFamily): a list of finite state machines that
            corresponds to the grammar;
        tier (list): list of tuples, where every tuple lists elements
            of some tier.
    Learning for k > 2 is not implemented: requires more theoretical work.
    """

    def __init__(
        self, alphabet=None, grammar=None, k=2, data=None, edges=[">", "<"], polar="p"
    ):
        """Initializes the TSL object."""
        super().__init__(alphabet, grammar, k, data, edges, polar)
        self.fsm = FSMFamily()
        if self.k != 2:
            raise NotImplementedError(
                "The learner for k-MTSL languages is " "still being designed."
            )
        self.tier = None

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
            raise ValueError(
                "The alphabet is empty. Provide data or "
                "run `grammar.extract_alphabet`."
            )

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
        self.tier = [i for i in self.grammar]

        if self.check_polarity() == "p":
            self.grammar = self.opposite_polarity()

    def scan(self, string):
        """Scan string with respect to a given MTSL grammar.

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
        """Gathers grammars with the same tier together.

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
        """Collects a list of paths from a string.

        A path is a
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
                path.append(list(set([k for k in string[(i + 1) : j]])))
                path.append(string[j])

                if path not in paths:
                    paths.append(path)

        return paths

    def all_paths(self, dataset):
        """Finds all paths that are present in a list of strings.

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
        """Generates a grammar of the opposite polarity.

        Returns:
            dict: a dictionary containing the opposite ngram lists
                for every tier of the grammar.
        """
        if not self.grammar:
            raise ValueError(
                "Grammar needs to be provided. It can also "
                "be learned using `grammar.learn()`."
            )
        opposite = {}
        for i in self.grammar:
            possib = self.generate_all_ngrams(list(i), self.k)
            opposite[i] = [j for j in possib if j not in self.grammar[i]]

        return opposite

    def switch_polarity(self):
        """Changes polarity of the grammar, and rewrites grammar to the
        opposite one."""
        self.grammar = self.opposite_polarity()
        self.change_polarity()

    def map_restrictions_to_fsms(self):
        """Maps restrictions to FSMs: based on the grammar, it creates a list
        of lists, where every sub-list has the following shape:

        [tier_n, restrictions_n, fsm_n]. Such sub-list is constructed
        for every single tier of the current MTSL grammar.
        Returns:
            [list, list, FSM]
                list: a list of current tier's symbols;
                list: a list of current tier's restrictions;
                FSM: a FSM corresponding to the current tier.
        """
        if not self.grammar:
            raise (IndexError("The grammar must not be empty."))

        restr_to_fsm = []

        for alpha, ngrams in self.grammar.items():
            polarity = self.check_polarity()
            tsl = TSL(
                self.alphabet,
                self.grammar,
                self.k,
                self.data,
                self.edges,
                polar=polarity,
            )
            if not tsl.alphabet:
                tsl.extract_alphabet()
            tsl.tier = list(alpha)
            tsl.grammar = list(ngrams)
            tsl.fsmize()
            restr_to_fsm.append([tsl.tier[:], tsl.grammar[:], tsl.fsm])

        return restr_to_fsm

    def fsmize(self):
        """Builds FSM family corresponding to the given grammar and saves in it
        the fsm attribute."""
        restr_to_fsm = self.map_restrictions_to_fsms()
        self.fsm.family = [i[2] for i in restr_to_fsm]

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
        if not self.fsm.family:
            self.fsmize()

        tier_smap = self.tier_state_maps()
        if not any([len(tier_smap[x]) for x in tier_smap]):
            raise (
                ValueError(
                    "There are ngrams in the grammar that are"
                    " not leading anywhere. Clean the grammar "
                    " or run `grammar.clean_grammar()`."
                )
            )

        data = [self.generate_item(tier_smap) for i in range(n)]

        if not repeat:
            data = set(data)
            useless_loops = 0
            prev_len = len(data)

            while len(data) < n:
                data.add(self.generate_item(tier_smap))

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

    def tier_image(self, string):
        """
        Creates tier images of a string with respect to the different
        tiers listed in the grammar.
        Returns:
            dict: a dictionary of the following shape:
                { (tier_1):"string_image_given_tier_1",
                    ...,
                  (tier_n):"string_image_given_tier_n"
                }
        """
        tiers = {}
        for i in self.grammar:
            curr_tier = ""
            for s in string:
                if s in self.edges or s in i:
                    curr_tier += s
            tiers[i] = curr_tier
        return tiers

    def generate_item(self, tier_smap):
        """Generates a well-formed string with respect to the given grammar.

        Returns:
            str: a well-formed string.
        """
        word = self.edges[0] * (self.k - 1)
        main_smap = self.general_state_map(tier_smap)
        tier_images = self.tier_image(word)

        while word[-1] != self.edges[1]:
            maybe = choice(main_smap[word[-(self.k - 1) :]])
            good = True
            for tier in tier_smap:
                if maybe in tier:
                    old_image = tier_images[tier]
                    if maybe not in tier_smap[tier][old_image[-(self.k - 1) :]]:
                        good = False
            if good:
                word += maybe
                tier_images = self.tier_image(word)

        newword = word[(self.k - 1) : -1]
        if self.scan(newword):
            return newword
        else:
            return self.generate_item(tier_smap)

    def tier_state_maps(self):
        """
        Generates a dictionary of transitions within the FSMs
        that correspond to the tier grammars.
        Returns:
            dict: the dictionary of the form
                {
                 (tier_1):{"keys":[list of next symbols]},
                 (tier_2):{"keys":[list of next symbols]},
                   ...
                 (tier_n):{"keys":[list of next symbols]},
                }, where keys are (k-1)-long tier representations.
        Warning: the list of next symbols is tier-specific,
            so this estimates the rough options: refer to
            generate_item for the filtering of wrongly
            generated items.
        """
        restr_to_fsm = self.map_restrictions_to_fsms()
        tier_smaps = {}

        for curr_tier in restr_to_fsm:
            sl = SL()
            sl.change_polarity(self.check_polarity())
            sl.edges = self.edges
            sl.k = self.k
            sl.alphabet = curr_tier[0]
            sl.grammar = curr_tier[1]
            sl.fsm = curr_tier[2]
            tier_smaps[tuple(sl.alphabet)] = sl.state_map()

        return tier_smaps

    def general_state_map(self, smaps):
        """
        Generates a dictionary of transitions within all
        FSMs of the FSM family.
        Returns:
            dict: the dictionary of the form
                {"keys":[list of next symbols]}, where 
                keys are (k-1)-long strings.
        Warning: the list of next symbols is tier-specific,
            so this estimates the rough options: refer to
            generate_item for the filtering of wrongly
            generated items.
        """
        local_smaps = deepcopy(smaps)

        for tier in local_smaps:
            non_tier = [i for i in self.alphabet if i not in tier]
            for entry in local_smaps[tier]:
                local_smaps[tier][entry].extend(non_tier)

        local_smaps = list(local_smaps.values())
        main_smap = deepcopy(local_smaps[0])

        for other in local_smaps[1:]:
            for entry in other:

                if entry not in main_smap:
                    main_smap[entry] = other[entry]
                else:
                    inter = [i for i in main_smap[entry] if i in other[entry]]
                    main_smap[entry] = inter

        free_ones = []
        for i in self.alphabet:
            for j in self.grammar:
                if i in j:
                    break
            free_ones.append(i)

        ext_alphabet = deepcopy(self.alphabet) + [self.edges[1]]
        for x in free_ones:
            main_smap[x] = ext_alphabet

        return main_smap

    def clean_grammar(self):
        """Removes useless ngrams from the grammar.

        If negative, it just removes duplicates. If positive, it detects
        ngrams to which one cannot get     from the initial symbol and
        from which one cannot get     to the final symbol, and removes
        them.
        """
        for tier in self.grammar:
            sl = SL()
            sl.change_polarity(self.check_polarity())
            sl.edges = self.edges
            sl.alphabet = list(tier)
            sl.k = self.k
            sl.grammar = self.grammar[tier]
            sl.fsmize()
            sl.clean_grammar()
            self.grammar[tier] = deepcopy(sl.grammar)
