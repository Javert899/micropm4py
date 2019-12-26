import time

# RAN ON CORTEX M3, 64kb RAM
def r(tr, p, on, row):
    if on == 2:
        if "concept:name" in row:
            p[1].append(row.split("\"")[3])
        elif "</event" in row:
            on = 1
    elif on == 1:
        if "<event" in row:
            on = 2
        elif "</trace" in row:
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


def main():
    tr = None
    p = None
    on = 0
    dfg = [[], dict(), set(), set(), dict()]
    tr, p, on = r(tr, p, on, "<?xml version='1.0' encoding='UTF-8'?>")
    tr, p, on = r(tr, p, on, "<log>")
    tr, p, on = r(tr, p, on, "\t<trace>")
    tr, p, on = r(tr, p, on, "\t\t<string key=\"concept:name\" value=\"ciao\" />")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"C\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t</trace>")
    print(tr)
    dfg = udf(dfg, tr[1])
    tr, p, on = r(tr, p, on, "\t<trace>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t</trace>")
    print(tr)
    dfg = udf(dfg, tr[1])
    tr, p, on = r(tr, p, on, "</log>")
    print(dfg)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
