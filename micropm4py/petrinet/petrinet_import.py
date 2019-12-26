import time

# RAN ON CORTEX M3, 64kb RAM
# Supports only visible transitions, and with arc weight equal to 1. Supports duplicate transitions.
def ip(n, im, fm, st, row):
    if "</transition" in row:
        st[0] = False
    elif "</initialMark" in row:
        st[3] = False
    elif "</finalmark" in row:
        st[1] = False
    if st[0]:
        if "<text" in row:
            st[2][n[1][-1][0]] = row.split("<text>")[1].split("</")[0]
    elif st[3]:
        if "<text" in row:
            im[len(n[0]) - 1] = int(row.split("<text>")[1].split("</")[0])
    elif st[1]:
        if "<place" in row:
            st[4] = n[0].index(row.split("idref=\"")[1].split("\"")[0])
        elif "<text" in row:
            fm[st[4]] = int(row.split("<text>")[1].split("</")[0])
    elif "<place" in row:
        n[0].append(row.split("\"")[1])
    elif "<arc" in row:
        rs = row.split("\"")
        so = rs[3]
        ta = rs[5]
        if so in n[0]:
            i = 0
            while i < len(n[1]):
                if n[1][i][0] == ta:
                    break
                i = i + 1
            n[1][i][1][n[0].index(so)] = 1
        else:
            i = 0
            while i < len(n[1]):
                if n[1][i][0] == so:
                    break
                i = i + 1
            n[1][i][2][n[0].index(ta)] = 1
    elif "<transition" in row:
        st[0] = True
        n[1].append([row.split("id=\"")[1].split("\"")[0], {}, {}])
    elif "<initialMark" in row:
        st[3] = True
    elif "<finalmark" in row:
        st[1] = True
    return n, im, fm, st


def main():
    n = [[], []]
    im = {}
    fm = {}
    st = [False, False, {}, False, None]
    n, im, fm, st = ip(n, im, fm, st, "<?xml version='1.0' encoding='UTF-8'?>")
    n, im, fm, st = ip(n, im, fm, st, "<pnml>")
    n, im, fm, st = ip(n, im, fm, st,
                       "<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">")
    n, im, fm, st = ip(n, im, fm, st, "<page id=\"n0\">")
    n, im, fm, st = ip(n, im, fm, st, "<place id=\"source\">")
    n, im, fm, st = ip(n, im, fm, st, "<name>")
    n, im, fm, st = ip(n, im, fm, st, "<text>source</text>")
    n, im, fm, st = ip(n, im, fm, st, "</name>")
    n, im, fm, st = ip(n, im, fm, st, "<initialMarking>")
    n, im, fm, st = ip(n, im, fm, st, "<text>1</text>")
    n, im, fm, st = ip(n, im, fm, st, "</initialMarking>")
    n, im, fm, st = ip(n, im, fm, st, "</place>")
    n, im, fm, st = ip(n, im, fm, st, "<place id=\"p1\">")
    n, im, fm, st = ip(n, im, fm, st, "<name>")
    n, im, fm, st = ip(n, im, fm, st, "<text>p1</text>")
    n, im, fm, st = ip(n, im, fm, st, "</name>")
    n, im, fm, st = ip(n, im, fm, st, "</place>")
    n, im, fm, st = ip(n, im, fm, st, "<place id=\"sink\">")
    n, im, fm, st = ip(n, im, fm, st, "<name>")
    n, im, fm, st = ip(n, im, fm, st, "<text>sink</text>")
    n, im, fm, st = ip(n, im, fm, st, "</name>")
    n, im, fm, st = ip(n, im, fm, st, "</place>")
    n, im, fm, st = ip(n, im, fm, st, "<transition id=\"A\">")
    n, im, fm, st = ip(n, im, fm, st, "<name>")
    n, im, fm, st = ip(n, im, fm, st, "<text>A</text>")
    n, im, fm, st = ip(n, im, fm, st, "</name>")
    n, im, fm, st = ip(n, im, fm, st, "</transition>")
    n, im, fm, st = ip(n, im, fm, st, "<arc id=\"ac1\" source=\"source\" target=\"A\"/>")
    n, im, fm, st = ip(n, im, fm, st, "<arc id=\"ac2\" source=\"A\" target=\"p1\"/>")
    n, im, fm, st = ip(n, im, fm, st, "<transition id=\"B\">")
    n, im, fm, st = ip(n, im, fm, st, "<name>")
    n, im, fm, st = ip(n, im, fm, st, "<text>B</text>")
    n, im, fm, st = ip(n, im, fm, st, "</name>")
    n, im, fm, st = ip(n, im, fm, st, "</transition>")
    n, im, fm, st = ip(n, im, fm, st, "<arc id=\"ac3\" source=\"p1\" target=\"B\"/>")
    n, im, fm, st = ip(n, im, fm, st, "<arc id=\"ac4\" source=\"B\" target=\"sink\"/>")
    n, im, fm, st = ip(n, im, fm, st, "</page>")
    n, im, fm, st = ip(n, im, fm, st, "<finalmarkings>")
    n, im, fm, st = ip(n, im, fm, st, "<marking>")
    n, im, fm, st = ip(n, im, fm, st, "<place idref=\"sink\">")
    n, im, fm, st = ip(n, im, fm, st, "<text>1</text>")
    n, im, fm, st = ip(n, im, fm, st, "</place>")
    n, im, fm, st = ip(n, im, fm, st, "</marking>")
    n, im, fm, st = ip(n, im, fm, st, "</finalmarkings>")
    n, im, fm, st = ip(n, im, fm, st, "</net>")
    n, im, fm, st = ip(n, im, fm, st, "</pnml>")
    i = 0
    while i < len(n[1]):
        n[1][i][0] = st[2][n[1][i][0]]
        i = i + 1
    print(n)
    print(st)
    print(im)
    print(fm)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
