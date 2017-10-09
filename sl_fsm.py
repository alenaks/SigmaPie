#!/bin/python3
# -*- coding: utf-8 -*-
# Subregular Toolkit: python sl_fsm.py module
# Author: Alena Aksenova

"""
Module that builds a Finite State Machine (FSM) for
given SL grammar.
"""


def safety_check(ngrams):
    """ Function that checks that argument is of the appropriate type. """
    
    if type(ngrams) not in [list, set, tuple]:
        raise TypeError("The type of ngrams must be list, set, or a tuple.")


def sl_to_fsm(ngrams):
    """ Function that turns SL grammar into FSM.
        For example, bigram "abc" becomes transition ("ab", "c", "bc"):
            after the sequence "ab" reading "c" brings you to the state "bc".
    """
    safety_check(ngrams)
    return [(ngram[:-1], ngram[-1], ngram[1:]) for ngram in grams]
           if ngrams !=[] else ngram


def trim_fsm(transitions, markers=[">", "<"]):
    """ This function trims useless states out of the FSA.
        The algorithm is made by Gordon Pace (University of Malta).
        Idea: find the initial state and collect the set of states to which
            one can come from that node and the nodes connected to it
            (detects all states to which one cannot get).
        My modification: change direction of the transitions and run the same
            algorithm again to detect states drom which one cannot get to
            the final state(s).
    """

    if transitions == []:
        return transitions

    # here we get rid of the non-entering states
    transitions = accessible_states(transitions, markers[0])

    # here we get rid of states that don't have access to the final state(s)
    mirrored_list = [(i[2], i[1], i[0]) for i in transitions]
    mirrored_list = accessible_states(mirrored_list, markers[1])
    return [(i[2], i[1], i[0]) for i in mirrored_list]


def accessible_states(transitions, marker):
    """ Find an initial state (transition) and see where it is
        possible to get from there. Return the list of transitions
        that can be accessed.
    """

    # make copies of the list of transitions to modify
    # and loop over them safely
    loop_trans, updated = transitions[:], transitions[:]

    # find initial transition(s)
    reachable = []
    for i in transitions:
        if i[0][0] == i[0][-1] and i[0][-1] == marker:
            reachable.append(i)
            loop_trans.remove(i)
            updated.remove(i)
    loop_reach = reachable[:]

    # while loop runs while something is changing in the transitions
    previous_step = []
    while previous_step != updated:
        previous_step = updated[:]
        for i in loop_trans:
            for j in loop_reach:
                if j[-1] == i[0]:
                    reachable.append(i)
                    updated.remove(i)
        loop_trans = updated[:]
        loop_reach = reachable[:]

    return reachable
    

def fsm_to_sl(transitions):
    """ Generates SL grammar based on the given transitions.
        For the transition ("ab", "c", "bc") gives ngram "abc".
    """
    
    if transitions == []:
        return transitions

    ngrams = []
    for i in transitions:
        ngram = "".join(i[:2])
        ngrams.append(ngram)

    return ngrams
