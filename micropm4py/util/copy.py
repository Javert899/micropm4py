# implementation of the Python basic copy (not available in Micropython) for dictionaries

def copy(dct):
    n = {}
    for k in dct:
        n[k] = dct[k]
    return n
