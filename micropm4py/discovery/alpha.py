def causal(dfg):
    c = [[], []]
    itms = []
    for el in dfg[4]:
        itms.append(el)
    i = 0
    while i < len(itms):
        rev_tup = (itms[i][1], itms[i][0])
        j = i + 1
        found = -1
        while j < len(itms):
            if rev_tup == itms[j]:
                found = j
            j = j + 1
        if found >= 0:
            c[1].append(itms[i])
            c[1].append(itms[found])
            del itms[found]
        else:
            c[0].append(itms[i])
        i = i + 1
    c[0] = tuple(c[0])
    c[1] = tuple(c[1])
    c = tuple(c)
    return c


def un(tup1, tup2):
    r = set()
    for el in tup1:
        r.add(el)
    for el in tup2:
        r.add(el)
    r = tuple(r)
    return r


def check_tup(tup, c):
    i = 0
    while i < len(tup[0]):
        j = i + 1
        while j < len(tup[0]):
            tc = (tup[0][i], tup[0][j])
            itc = (tup[0][j], tup[0][i])
            if tc in c[0] or itc in c[0] or tc in c[1]:
                return False
            j = j + 1
        i = i + 1
    i = 0
    while i < len(tup[1]):
        j = i + 1
        while j < len(tup[1]):
            tc = (tup[1][i], tup[1][j])
            itc = (tup[1][j], tup[1][i])
            if tc in c[0] or itc in c[0] or tc in c[1]:
                return False
            j = j + 1
        i = i + 1
    i = 0
    while i < len(tup[0]):
        j = 0
        while j < len(tup[1]):
            tc = (tup[0][i], tup[1][j])
            if tc not in c[0]:
                return False
            j = j + 1
        i = i + 1
    return True


def cont(tup1, tup2):
    for el in tup1[0]:
        if el not in tup2[0]:
            return False
    for el in tup1[1]:
        if el not in tup2[1]:
            return False
    return True


def alpha(dfg):
    c = causal(dfg)
    net = [["source", "sink"], []]
    im = {0: 1}
    fm = {1: 1}
    pls = []
    i = 0
    while i < len(c[0]):
        pls.append(((c[0][i][0], ), (c[0][i][1], )))
        i = i + 1
    shall_continue = True
    while shall_continue:
        shall_continue = False
        i = 0
        while i < len(pls):
            j = i + 1
            found = False
            while j < len(pls):
                unt = (un(pls[i][0], pls[j][0]), un(pls[i][1], pls[j][1]))
                if unt != pls[i] and unt != pls[j]:
                    if check_tup(unt, c):
                        del pls[i]
                        del pls[j-1]
                        pls.append(unt)
                        found = True
                        shall_continue = True
                        break
                j = j + 1
            if found:
                break
            i = i + 1
    shall_continue = True
    while shall_continue:
        shall_continue = False
        i = 0
        while i < len(pls):
            j = i + 1
            while j < len(pls):
                if cont(pls[i], pls[j]):
                    del pls[i]
                    shall_continue = True
                    break
                elif cont(pls[j], pls[i]):
                    del pls[j]
                    break
                j = j + 1
            if shall_continue:
                break
            i = i + 1
    i = 0
    while i < len(pls):
        net[0].append("p%d" % i)
        i = i + 1
    i = 0
    while i < len(dfg[0]):
        tr = [dfg[0][i], [], []]
        j = 0
        while j < len(pls):
            if i in pls[j][0]:
                tr[2].append(j+2)
            if i in pls[j][1]:
                tr[1].append(j+1)
            j = j + 1
        if i in dfg[2]:
            tr[1].append(0)
        if i in dfg[3]:
            tr[2].append(1)
        tr[1] = tuple(tr[1])
        tr[2] = tuple(tr[2])
        tr = tuple(tr)
        net[1].append(tr)
        i = i + 1
    net[0] = tuple(net[0])
    net[1] = tuple(net[1])
    net = tuple(net)
    return net, im, fm
