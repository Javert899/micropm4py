from micropm4py.petrinet import petrinet_import


# Supports only visible transitions, and with arc weight equal to 1. Supports duplicate transitions.
def imp_file(file_path):
    n = [[], []]
    im = {}
    fm = {}
    st = [False, False, {}, False, None, {}]
    F = open(file_path, "r")
    line = F.readline()
    while line:
        petrinet_import.ip(n, im, fm, st, line)
        line = F.readline()
    F.close()
    petrinet_import.finish_net(n, st)
    return n, im, fm
