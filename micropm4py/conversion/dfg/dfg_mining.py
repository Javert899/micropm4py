def apply(dfg):
    n = [[], []]
    im = {}
    fm = {}
    if len(dfg[2]) > 1 or len(dfg[3]) > 1:
        raise Exception("only DFGs with a single start activity/end activity are now supported! Try to add artificial start/end activities")
    for act in dfg[0]:
        n[0].append(act)
    for tup in dfg[4]:
        n[1].append((dfg[0][tup[1]], (tup[0],), (tup[1],)))
    n[0].append("@@source@@")
    n[1].append((dfg[0][list(dfg[2])[0]], (len(n[0])-1,), (list(dfg[2])[0],)))
    n[0] = tuple(n[0])
    n[1] = tuple(n[1])
    im[len(n[0])-1] = 1
    fm[list(dfg[3])[0]] = 1
    n = tuple(n)
    return n, im, fm
