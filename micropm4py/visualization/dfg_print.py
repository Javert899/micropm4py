import time

# RAN ON CORTEX M3, 64kb RAM


def prnt_dot(dfg):
    print("digraph graphname {")
    i = 0
    while i < len(dfg[0]):
        print("%d [label=\"%s (%d)\"];" % (i, dfg[0][i], dfg[1][i]))
        i = i + 1
    for tup in dfg[4]:
        print("%d -> %d [label=\"%d\"];" % (tup[0], tup[1], dfg[4][tup]))
    print("}")


def main():
    dfg = [("A", "B", "C"), {0: 2, 1: 2, 2: 1}, tuple({0}), tuple({1, 2}), {(0, 1): 2, (1, 2): 1}]
    prnt_dot(dfg)


if __name__ == "__main__":
    aa = time.ticks_ms()
    main()
    bb = time.ticks_ms()
    print(bb-aa)
