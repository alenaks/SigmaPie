#!/bin/python3

"""
   An implementation of the learning algorithm OSTIA.
   Copyright (C) 2019  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from fst_object import *
from helper import *


def ostia(S, Sigma, Gamma):
    """
    This function implements OSTIA (Onward Subsequential Transduction
    Inference Algorithm).

    Input:
        S (list): a list of pairs (o, t), where `o` is the original
            string, and `t` is its translation;
        Sigma (list): the input alphabet;
        Gamma (list): the output alphabet.
    """

    # create a template of the onward PTT
    T = build_ptt(S, Sigma, Gamma)
    T = onward_ptt(T, "", "")[0]
    
    # color the nodes
    red = [""]
    blue = [tr[3] for tr in T.E if tr[0] == "" and len(tr[1]) == 1]
    
    # choose a blue state
    while len(blue) != 0:
        blue_state = blue[0]

        # if exists state that we can merge with, do it
        exists = False
        for red_state in red:
            
            # if you already merged that blue state with something, stop
            if exists == True: break
                
            # try to merge these two states
            if ostia_merge(T, red_state, blue_state):
                T = ostia_merge(T, red_state, blue_state)
                exists = True
        
        # if it is not possible, color that blue state red
        if not exists:
            red.append(blue_state)
            
        # if possible, remove the folded state from the list of states
        else:
            T.Q.remove(blue_state)
            del T.stout[blue_state]
            
        # add in blue list other states accessible from the red ones that are not red
        blue = []
        for tr in T.E:
            if tr[0] in red and tr[3] not in red:
                blue.append(tr[3])
    
    # clean the transducer from non-reachable states
    T = ostia_clean(T)
                
    return T


def build_ptt(S, Sigma, Gamma):
    """
    Builds a prefix tree transducer based on the data sample.

    Input:
        S (list): a list of pairs (o, t), where `o` is the original
            string, and `t` is its translation;
        Sigma (list): the input alphabet;
        Gamma (list): the output alphabet.
    """
    
    # build a template for the transducer
    T = FST(Sigma, Gamma)
    
    # fill in the states of the transducer
    T.Q = []
    for i in S:
        for j in prefix(i[0]):
            if j not in T.Q:
                T.Q.append(j)
                
    # fill in the empty transitions
    T.E = []
    for i in T.Q:
        if len(i) >= 1:
            T.E.append([i[:-1], i[-1], "", i])
            
    # fill in state outputs
    T.stout = {}
    for i in T.Q:
        for j in S:
            if i == j[0]:
                T.stout[i] = j[1]
        if i not in T.stout:
            T.stout[i] = "*"
    
    return T




def onward_ptt(T, q, u):
    """ Makes the PTT onward. """
    
    # proceed as deep as possible
    for tr in T.E:
        if tr[0] == q:
            T, qx, w = onward_ptt(T, tr[3], tr[1])
            if tr[2] != "*":
                tr[2] += w
                  
    # find lcp of all ways of leaving state 1 or stopping in it
    t = [tr[2] for tr in T.E if tr[0] == q]
    f = lcp(T.stout[q], *t)
    
    # remove from the prefix unless it's the initial state
    if f != "" and q != "":
        for tr in T.E:
            if tr[0] == q:
                tr[2] = remove_from_prefix(tr[2], f)
        T.stout[q] = remove_from_prefix(T.stout[q], f)
                
    return T, q, f




def ostia_outputs(w1,w2):
    ''' Compares two strings allowing for unknown. '''
    
    if w1 == "*": return w2
    elif w2 == "*": return w1
    elif w1 == w2: return w2
    else: return False





def ostia_pushback(T_orig, q1, q2, a):
    ''' Moves further the part after lcp of two states. '''
    
    # to avoid rewriting the original transducer
    T = copy_fst(T_orig)
    
    # states where you get if follow a
    q1_goes_to = None
    q2_goes_to = None
    
    # what is being written from this state
    from_q1, from_2 = None, None
    for tr in T.E:
        if tr[0] == q1 and tr[1] == a:
            from_q1 = tr[2]
            q1_goes_to = tr[3]
        if tr[0] == q2 and tr[1] == a:
            from_q2 = tr[2]
            q2_goes_to = tr[3]
    if from_q1 == None or from_q2 == None:
        raise ValueError("One of the states cannot be found.")
    
    # find the part after longest common prefix
    u = lcp(from_q1, from_q2)
    remains_q1 = from_q1[len(u):]
    remains_q2 = from_q2[len(u):]
    
    # assign lcp as current output
    for tr in T.E:
        if tr[0] in [q1, q2] and tr[1] == a:
            tr[2] = u
            
    # find what the next state writes given any other choice
    # and append the common part in it
    for tr in T.E:
        if tr[0] == q1_goes_to:
            tr[2] = remains_q1 + tr[2]
        if tr[0] == q2_goes_to:
            tr[2] = remains_q2 + tr[2]
    
    # append common part to the next state's state output
    if T.stout[q1_goes_to] != "*":
        T.stout[q1_goes_to] = remains_q1 + T.stout[q1_goes_to]
    if T.stout[q2_goes_to] != "*":
        T.stout[q2_goes_to] = remains_q2 + T.stout[q2_goes_to]
    
    return T




def ostia_merge(T_orig, q1, q2):
    ''' Redirects all branches to q2 into q1. '''
    
    # to avoid rewriting the original transducer
    T = copy_fst(T_orig)
    
    # save which transition was changed to revert in case cannot merge the states
    changed = None
    for tr in T.E:
        if tr[3] == q2:
            changed = tr[:]
            tr[3] = q1
            
    # save the state output of the q1 originally
    changed_stout = T.stout[q1]
            
    # check if we can merge the states
    can_do = ostia_fold(T, q1, q2)
    
    # if cannot, revert the change
    if can_do == False:
        for tr in T.E:
            if tr[0] == changed[0] and tr[1] == changed[1] and tr[2] == changed[2]:
                tr[3] = changed[3]
        T.stout[q1] = changed_stout
        return False
    
    # if can, do it
    else: return can_do




def ostia_fold(T_orig, q1, q2):
    ''' Folds recursively subtrees of Q2 into Q1. '''
    
    # to avoid rewriting the original transducer
    T = copy_fst(T_orig)
    
    # compare the state outputs
    w = ostia_outputs(T.stout[q1], T.stout[q2])
    if w == False: return False
    
    # rewrite * in case it's the output of q1
    T.stout[q1] = w

    # look at every possible subtree of q_2
    for a in T.Sigma:
        add_new = False

        for tr_2 in T.E:
            if tr_2[0] == q2 and tr_2[1] == a:
                
                # if the edge exists from q1
                edge_defined = False
                for tr_1 in T.E:
                    if tr_1[0] == q1 and tr_1[1] == a:
                        edge_defined = True
                        
                        # fail if inconsistent with output of q2
                        if tr_1[2] not in prefix(tr_2[2]):
                            return False
                        
                        # move the mismatched suffix of q1 and q2 further
                        T = ostia_pushback(T, q1, q2, a)
                        T = ostia_fold(T, tr_1[3], tr_2[3])
                        if T == False: return False
                        
                # if the edge doesn't exist from q1 yet, add it
                if not edge_defined:
                    add_new = [q1, a, tr_2[2], tr_2[3]]
        
        # if the new transition was constructed, add it to the list of transitions
        if add_new:
            T.E.append(add_new)
    
    return T




def ostia_clean(T_orig):
    ''' Cleans the resulting transducers by getting rid of the states that were never processed
        (i.e. never colored red or blue) -- those states are not reachable from the initial state.
    '''
    
    # to avoid rewriting the original transducer
    T = copy_fst(T_orig)
    
    # determine which states are reachable, i.e. accessible from the initial state
    reachable_states = [""]
    add = []
    change_made = True
    while change_made == True:
        change_made = False
        for st in reachable_states:
            for tr in T.E:
                if tr[0] == st and tr[3] not in reachable_states and tr[3] not in add:
                    add.append(tr[3])
                    change_made = True

        # break out of the loop if after checking the list once again, no states were added
        if change_made == False:
            break
        else:
            reachable_states.extend(add)
            add = []
            
    # clean the list of transitions
    new_E = []
    for tr in T.E:
        if tr[0] in reachable_states and tr[3] in reachable_states:
            new_E.append(tr)
    T.E = new_E

    # clean the dictionary of state outputs
    new_stout = {}
    for i in T.stout:
        if i in reachable_states:
            new_stout[i] = T.stout[i]
    T.stout = new_stout

    # clean the list of states
    new_Q = [i for i in T.Q if i in reachable_states]
    T.Q = new_Q
    
    return T





