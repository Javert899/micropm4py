import time

# RAN ON CORTEX M3, 64kb RAM
def import_header(l, sep, ci, ai):
    l = l.split(sep)
    cidp = -1
    acp = -1
    i = 0
    while i < len(l):
        if l[i] == ci:
            cidp = i
        elif l[i] == ai:
            acp = i
        i = i + 1
    return cidp, acp


def import_traces(d, l, sep, cidp, acp, da):
    l = l.rstrip().split(sep)
    if l[cidp] not in d:
        d[l[cidp]] = []
    a = l[acp]
    if a not in da:
        da[a] = a
    d[l[cidp]].append(da[a])
    return d


def finish_traces(d):
    r = []
    vv = {}
    kk = list(d.keys())
    while kk:
        d[kk[0]] = tuple(d[kk[0]])
        if d[kk[0]] not in vv:
            vv[d[kk[0]]] = d[kk[0]]
        r.append((kk[0], vv[d[kk[0]]]))
        del d[kk[0]]
        del kk[0]
    return r


def import_dfg(dfg, d, l, sep, cidp, acp):
    l = l.rstrip().split(sep)
    a = l[acp]
    if a not in dfg[0]:
        dfg[0].append(a)
        dfg[1][len(dfg[0])-1] = 0
    dfg[1][dfg[0].index(a)] = dfg[1][dfg[0].index(a)] + 1
    if l[cidp] not in d:
        dfg[2].add(dfg[0].index(a))
    else:
        tup = (dfg[0].index(d[l[cidp]]), dfg[0].index(a))
        if tup not in dfg[4]:
            dfg[4][tup] = 0
        dfg[4][tup] = dfg[4][tup] + 1
    d[l[cidp]] = a
    return dfg, d


def import_dfg_sten(dfg, d, l, sep, cidp, acp):
    l = l.rstrip().split(sep)
    a = l[acp]
    if a not in dfg[0]:
        dfg[0].append(a)
        dfg[1][len(dfg[0])-1] = 0
    dfg[1][dfg[0].index(a)] = dfg[1][dfg[0].index(a)] + 1
    if l[cidp] not in d:
        d[l[cidp]] = ">>"
        dfg[1][0] = dfg[1][0] + 1
    tup = (dfg[0].index(d[l[cidp]]), dfg[0].index(a))
    if tup not in dfg[4]:
        dfg[4][tup] = 0
    dfg[4][tup] = dfg[4][tup] + 1
    d[l[cidp]] = a
    return dfg, d


def finish_dfg(dfg, d):
    for c in d:
        dfg[3].add(dfg[0].index(d[c]))
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    return dfg


def finish_dfg_sten(dfg, d):
    for c in d:
        tup = (dfg[0].index(d[c]), dfg[0].index("[]"))
        if tup not in dfg[4]:
            dfg[4][tup] = 0
        dfg[4][tup] = dfg[4][tup] + 1
        dfg[1][1] = dfg[1][1] + 1
    return dfg


def main():
    cidp, acp = import_header("case:concept:name,concept:name", ",", "case:concept:name", "concept:name")
    d = {}
    da = {}
    d = import_traces(d, "1,A", ",", cidp, acp, da)
    d = import_traces(d, "2,A", ",", cidp, acp, da)
    d = import_traces(d, "1,B", ",", cidp, acp, da)
    d = import_traces(d, "2,B", ",", cidp, acp, da)
    d = import_traces(d, "1,C", ",", cidp, acp, da)
    d = finish_traces(d)
    print(d)


def main2():
    cidp, acp = import_header("case:concept:name,concept:name", ",", "case:concept:name", "concept:name")
    dfg = [[], dict(), set(), set(), dict()]
    d = {}
    dfg, d = import_dfg(dfg, d, "1,A", ",", cidp, acp)
    dfg, d = import_dfg(dfg, d, "2,A", ",", cidp, acp)
    dfg, d = import_dfg(dfg, d, "1,B", ",", cidp, acp)
    dfg, d = import_dfg(dfg, d, "2,B", ",", cidp, acp)
    dfg, d = import_dfg(dfg, d, "1,C", ",", cidp, acp)
    dfg = finish_dfg(dfg, d)
    print(dfg)


def main3():
    cidp, acp = import_header("case:concept:name,concept:name", ",", "case:concept:name", "concept:name")
    dfg = [[">>", "[]"], {0: 0, 1: 0}, {0}, {1}, dict()]
    d = {}
    dfg, d = import_dfg_sten(dfg, d, "1,A", ",", cidp, acp)
    dfg, d = import_dfg_sten(dfg, d, "2,A", ",", cidp, acp)
    dfg, d = import_dfg_sten(dfg, d, "1,B", ",", cidp, acp)
    dfg, d = import_dfg_sten(dfg, d, "2,B", ",", cidp, acp)
    dfg, d = import_dfg_sten(dfg, d, "1,C", ",", cidp, acp)
    dfg = finish_dfg_sten(dfg, d)
    print(dfg)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main3()
    bb = time.ticks_ms()
    print(bb-aa)
