def r(tr, p, on, row, d):
    if on == 2:
        if "concept:name" in row:
            a = row.split("\"")[3]
            if a not in d:
                d[a] = a
            p[1].append(d[a])
        elif "</event" in row:
            on = 1
    elif on == 1:
        if "<event" in row:
            on = 2
        elif "</trace" in row:
            p[1] = tuple(p[1])
            tr = p
            p = None
            on = 0
        elif "concept:name" in row:
            p[0] = row.split("\"")[3]
    else:
        tr = None
        if "<trace" in row:
            p = ["", []]
            on = 1
    return tr, p, on


def udf(dfg, tr):
    if len(tr) > 0:
        i = 0
        while i < len(tr):
            if not tr[i] in dfg[0]:
                dfg[0].append(tr[i])
                dfg[1][len(dfg[0]) - 1] = 0
            dfg[1][dfg[0].index(tr[i])] = dfg[1][dfg[0].index(tr[i])] + 1
            if i > 0:
                tup = (dfg[0].index(tr[i - 1]), dfg[0].index(tr[i]))
                if tup not in dfg[4]:
                    dfg[4][tup] = 0
                dfg[4][tup] = dfg[4][tup] + 1
            i = i + 1
        dfg[2].add(dfg[0].index(tr[0]))
        dfg[3].add(dfg[0].index(tr[-1]))
    return dfg


def udf_sten(dfg, tr):
    if len(tr) > 0:
        tr = [">>"] + list(tr) + ["[]"]
        i = 0
        while i < len(tr):
            if not tr[i] in dfg[0]:
                dfg[0].append(tr[i])
                dfg[1][len(dfg[0]) - 1] = 0
            dfg[1][dfg[0].index(tr[i])] = dfg[1][dfg[0].index(tr[i])] + 1
            if i > 0:
                tup = (dfg[0].index(tr[i - 1]), dfg[0].index(tr[i]))
                if tup not in dfg[4]:
                    dfg[4][tup] = 0
                dfg[4][tup] = dfg[4][tup] + 1
            i = i + 1
        dfg[2].add(dfg[0].index(tr[0]))
        dfg[3].add(dfg[0].index(tr[-1]))
    return dfg
