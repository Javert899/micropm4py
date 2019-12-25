from micropm4py.petrinet import petrinet_import


# Supports only visible transitions, and with arc weight equal to 1. Supports duplicate transitions.
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
    i = 0
    while i < len(n[1]):
        n[1][i][0] = st[2][n[1][i][0]]
        i = i + 1
    return n, im, fm
