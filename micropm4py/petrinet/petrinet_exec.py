def exec(p, m, a):
    for t in p[1]:
        if t[0] == a:
            o = True
            for p in t[1]:
                if p not in m:
                    o = False
                    break
            if o:
                for p in t[1]:
                    m[p] = m[p] - 1
                    if m[p] == 0:
                        del m[p]
                for p in t[2]:
                    if p not in m:
                        m[p] = 0
                    m[p] = m[p] + 1
                return m


def ex_trace(p, m, fm, tr):
    for act in tr:
        m = exec(p, m, act)
        if m is None:
            return False
    return m == fm
