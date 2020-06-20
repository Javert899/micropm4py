def prnt_dot(dfg):
    print("digraph graphname {")
    i = 0
    while i < len(dfg[0]):
        print("%d [label=\"%s (%d)\"];" % (i, dfg[0][i], dfg[1][i]))
        i = i + 1
    for tup in dfg[4]:
        print("%d -> %d [label=\"%d\"];" % (tup[0], tup[1], dfg[4][tup]))
    print("}")
