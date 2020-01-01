import time

# RAN ON CORTEX M3, 64kb RAM
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

def main():
    tr = None
    p = None
    on = 0
    dfg = [[], dict(), set(), set(), dict()]
    d = {}
    tr, p, on = r(tr, p, on, "<?xml version='1.0' encoding='UTF-8'?>", d)
    tr, p, on = r(tr, p, on, "<log>", d)
    tr, p, on = r(tr, p, on, "\t<trace>", d)
    tr, p, on = r(tr, p, on, "\t\t<string key=\"concept:name\" value=\"ciao\" />", d)
    tr, p, on = r(tr, p, on, "\t\t<event>", d)
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />", d)
    tr, p, on = r(tr, p, on, "\t\t</event>", d)
    tr, p, on = r(tr, p, on, "\t\t<event>", d)
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />", d)
    tr, p, on = r(tr, p, on, "\t\t</event>", d)
    tr, p, on = r(tr, p, on, "\t\t<event>", d)
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"C\" />", d)
    tr, p, on = r(tr, p, on, "\t\t</event>", d)
    tr, p, on = r(tr, p, on, "\t</trace>", d)
    print(tr)
    dfg = udf_sten(dfg, tr[1])
    tr, p, on = r(tr, p, on, "\t<trace>", d)
    tr, p, on = r(tr, p, on, "\t\t<event>", d)
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />", d)
    tr, p, on = r(tr, p, on, "\t\t</event>", d)
    tr, p, on = r(tr, p, on, "\t\t<event>", d)
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />", d)
    tr, p, on = r(tr, p, on, "\t\t</event>", d)
    tr, p, on = r(tr, p, on, "\t</trace>", d)
    print(tr)
    dfg = udf_sten(dfg, tr[1])
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    tr, p, on = r(tr, p, on, "</log>", d)
    print(dfg)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
