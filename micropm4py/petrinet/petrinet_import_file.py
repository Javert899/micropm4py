from micropm4py.petrinet import petrinet_import

def imp_file(file_path):
    n = [[], []]
    im = {}
    fm = {}
    st = [False, False, {}, False, None]
    F = open(file_path, "r")
    line = F.readline()
    while line:
        n, im, fm, st = petrinet_import.ip(n, im, fm, st, line)
        line = F.readline()
    F.close()
    return n, im, fm
