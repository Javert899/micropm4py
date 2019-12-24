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
            im[len(n[0])-1] = int(row.split("<text>")[1].split("</")[0])
    elif st[1]:
        if "<place" in row:
            st[4] = n[0].index(row.split("idref=\"")[1].split("\"")[0])
        elif "<text" in row:
            fm[st[4]] = int(row.split("<text>")[1].split("</")[0])
    elif "<place" in row:
        n[0].append(row.split("id=\"")[1].split("\"")[0])
    elif "<arc" in row:
        so = row.split("source=\"")[1].split("\"")[0]
        ta = row.split("target=\"")[1].split("\"")[0]
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

n = [[], []]
im = {}
fm = {}
st = [False, False, {}, False, None]
n, im, fm, st = ip(n, im, fm, st, "<?xml version='1.0' encoding='UTF-8'?>")
n, im, fm, st = ip(n, im, fm, st, "<pnml>")
n, im, fm, st = ip(n, im, fm, st, "<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">")
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
print(im)
print(fm)
del ip

def r(tr, p, on, row):
    if on == 2:
        if "concept:name" in row:
            p.append(row.split("value=\"")[1].split("\"")[0])
        elif "</event" in row:
            on = 1
    elif on == 1:
        if "<event" in row:
            on = 2
        elif "</trace" in row:
            tr = p
            p = None
            on = 0
    else:
        tr = None
        if "<trace" in row:
            p = []
            on = 1
    return tr, p, on

def exec(p, m, a):
    for t in p[1]:
        if t[0] == a:
            o = True
            for p, v in t[1].items():
                if p not in m or v < m[p]:
                    o = False
                    break
            if o:
                for p, v in t[1].items():
                    m[p] = m[p] - v
                    if m[p] == 0:
                        del m[p]
                for p, v in t[2].items():
                    if p not in m:
                        m[p] = 0
                    m[p] = m[p] + v
                return m

def ex_trace(p, m, fm, tr):
    for act in tr:
        m = exec(p, m, act)
        if m is None:
            return False
    return m == fm

def copy(dct):
    n = {}
    for k in dct:
        n[k] = dct[k]
    return n

tr = None
p = None
on = 0
tr, p, on = r(tr, p, on, "<?xml version='1.0' encoding='UTF-8'?>")
tr, p, on = r(tr, p, on, "<log>")
tr, p, on = r(tr, p, on, "\t<trace>")
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
print(ex_trace(n, copy(im), copy(fm), tr))
tr, p, on = r(tr, p, on, "\t<trace>")
tr, p, on = r(tr, p, on, "\t\t<event>")
tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />")
tr, p, on = r(tr, p, on, "\t\t</event>")
tr, p, on = r(tr, p, on, "\t\t<event>")
tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />")
tr, p, on = r(tr, p, on, "\t\t</event>")
tr, p, on = r(tr, p, on, "\t</trace>")
print(tr)
print(ex_trace(n, copy(im), copy(fm), tr))
tr, p, on = r(tr, p, on, "</log>")

