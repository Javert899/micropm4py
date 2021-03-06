def tr_to_dfg0(tr, dfg):
    if len(tr) > 0:
        i = 0
        while i < len(tr):
            if tr[i] not in dfg[0]:
                dfg[0].append(tr[i])
                dfg[1][len(dfg[0]) - 1] = 0
            dfg[1][dfg[0].index(tr[i])] = dfg[1][dfg[0].index(tr[i])] + 1
            if i > 0:
                tup = (dfg[0].index(tr[i - 1]), dfg[0].index(tr[i]))
                if not tup in dfg[4]:
                    dfg[4][tup] = 0
                dfg[4][tup] = dfg[4][tup] + 1
            i = i + 1
        dfg[2].add(dfg[0].index(tr[0]))
        dfg[3].add(dfg[0].index(tr[-1]))
    return dfg


def tr_to_dfg(tr, dfg):
    if len(tr) == 2 and type(tr[1]) is tuple:
        return tr_to_dfg0(tr[1], dfg)
    return tr_to_dfg0(tr, dfg)


def trs_to_dfg(trs):
    dfg = [[], dict(), set(), set(), dict()]
    for tr in trs:
        dfg = tr_to_dfg(tr, dfg)
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    dfg = tuple(dfg)
    return dfg
