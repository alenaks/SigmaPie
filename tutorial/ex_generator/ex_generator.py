from random import choice

def generate(n, specifications):
    """ Generates an n-long word based on the specified categories. """
    specified = list(map(choice, specifications.keys()))
    return "".join([choice(specified) for i in range(n)])

def generate_words(m, n, specifications):
    """ Generates m n-long words based on the specified categories. """
    return [generate(n, specifications) for i in range(m)]

def mask(w, specifications):
    """ Masks all non-initial mentions of the specified allophone. """
    classes = {i:False for i in specifications.keys()}
    new = ""
    for s in w:
        for c in classes:
            if s in c and not classes[c]:
                classes[c] = True
                new += s
            elif s in c:
                new += specifications[c]
    return new

def mask_words(words, specifications):
    """ Masks every word of a given list. """
    return [mask(w, specifications) for w in words]

def generate_pairs(m, n, specifications):
    """ Generates m pairs of n-long words. """
    outputs = generate_words(m, n, specifications)
    inputs = mask_words(outputs, specifications)
    return list(zip(inputs, outputs))
