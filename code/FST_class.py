class FST(object):

    def __init__(self, inalph=None, outalph=None, states=None, transitions=None):

        if inalph == None: self.inalph = []
        else: self.inalph = inalph

        if outalph == None: self.outalph = []
        else: self.outalph = outalph

        if states == None: self.states = dict()
        else: self.states = states

        if transitions == None: self.transitions = []
        else: self.transitions = transitions
