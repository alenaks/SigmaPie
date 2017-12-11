class A(object):
    """ Update each other """
    
    def __init__(self,percent=0):
        self.percent = percent

    @property
    def remainer(self):
        return 100 - self.percent

    @remainer.setter
    def remainer(self, value):
        self.percent = 100 - value



class Test(object):
    """ Calling one upates the other one """

    def __init__(self, data=None):
        self.data = data

    @property
    def alphabet(self):
        return self.alphabetize(self.data)

    @alphabet.setter
    def alphabet(self, value):
        self.alphabet = value


    def alphabetize(self, data):
        alph = []
        for i in data:
            alph += [j for j in i]
            
        return list(set(alph))


class Other(Test):
    def __init__(self, data=None):
        super().__init__(data)




def dosmth(l=[]):
    """ Dangerous lists in f definitions """
    l.append(3)
    return l
