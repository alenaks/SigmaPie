## =============================================== ##
## ==================== OSTIA ==================== ##
## =============================================== ##

def build_ptt(T, data):
    """ Function builds a PTT out of the data.
        Not that the PTT is not onward yet!

        -- T [FST] : transducer (template needs to be pre-created)
        -- data [dict] : training sample, in a form of the dictionary
    """

    # first create states by listing every prefix in
    # the input side of the sample, initialize the
    # state output to "don't know" = "*"
    for i in data:
        for j in pref(i):
            T.states[j] = "*"

    # draw transitions between the states: for every state
    # ua where len(a) = 1, make a transition [u, a, "", ua]
    for s in T.states:
        if s != "":
            tran = [s[:-1], s[-1], "", s]
            T.transitions.append(tran)

    # to the states that correspond to some data item, instantiate
    # their state output as the output side of the corresponding item
    for s in T.states:
        if s in data:
            T.states[s] = data[s]
            
    return T


def ostia_learn(T, data):
    T = build_ptt(T, data)
    return T


def onward_ptt(T, q="", s=""):
    """ Thie function makes the transducer onward.

        -- T [FST] : 
    """
    
    pass



## ================================================ ##
## =============== HELPER FUNCTIONS =============== ##
## ================================================ ##   

def pref(s):
    """ Returns a list of prefixes for a given string.
        -- s [str] : string that needs to be processed
    """
    return [s[:i] for i in range(len(s)+1)]
