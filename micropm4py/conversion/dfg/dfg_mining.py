import time

# RAN ON CORTEX M3, 64kb RAM
def apply(dfg):
    n = [[], []]
    im = {}
    fm = {}
    if len(dfg[2]) > 1 or len(dfg[3]) > 1:
        raise Exception("only DFGs with a single start activity/end activity are now supported! Try to add artificial start/end activities")
    for act in dfg[0]:
        n[0].append(act)
    for tup in dfg[4]:
        n[1].append((dfg[0][tup[1]], (tup[0],), (tup[1],)))
    n[0].append("@@source@@")
    n[1].append((dfg[0][list(dfg[2])[0]], (len(n[0])-1,), (list(dfg[2])[0],)))
    n[0] = tuple(n[0])
    n[1] = tuple(n[1])
    im[len(n[0])-1] = 1
    fm[list(dfg[3])[0]] = 1
    return n, im, fm


def main():
    dfg = [("A", "B", "C"), {0:1, 1:1, 2:1}, tuple({0}), tuple({2}), {(0, 1): 1, (1, 2): 1}]
    n, im, fm = apply(dfg)
    print(n)
    print(im)
    print(fm)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
