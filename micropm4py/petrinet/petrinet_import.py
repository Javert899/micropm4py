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
            tn = row.split("<text>")[1].split("</")[0]
            if tn not in st[5]:
                st[5][tn] = tn
            st[2][n[1][-1][0]] = st[5][tn]
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
            n[1][i][1].append(n[0].index(so))
        else:
            i = 0
            while i < len(n[1]):
                if n[1][i][0] == so:
                    break
                i = i + 1
            n[1][i][2].append(n[0].index(ta))
    elif "<transition" in row:
        st[0] = True
        n[1].append([row.split("id=\"")[1].split("\"")[0], [], []])
    elif "<initialMark" in row:
        st[3] = True
    elif "<finalmark" in row:
        st[1] = True


def finish_net(n, st):
    lenn = len(n[0])
    n[0] = []
    x = 0
    i = 0
    while i < lenn:
        n[0].append(x)
        i = i + 1
    n[0] = tuple(n[0])
    i = 0
    while i < len(n[1]):
        n[1][i][0] = st[2][n[1][i][0]]
        n[1][i][1] = tuple(n[1][i][1])
        n[1][i][2] = tuple(n[1][i][2])
        n[1][i] = tuple(n[1][i])
        i = i + 1
    n[1] = tuple(n[1])
