import time

# RAN ON CORTEX M3, 64kb RAM
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


def main():
    p = [["source", "p1", "sink"], [["A", {0: 1}, {1: 1}], ["B", {1: 1}, {2: 1}]]]
    r = ex_trace(p, {0: 1}, {2: 1}, ["A", "B"])
    print(r)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
