def print_dot(net):
    print("digraph graphname {")
    i = 0
    while i < len(net[0]):
        print("p%d [label=\"\"];" % (i,))
        i = i + 1
    i = 0
    while i < len(net[1]):
        print("t%d [label=\"%s\", shape=box];" % (i, net[1][i][0]))
        i = i + 1
    i = 0
    while i < len(net[1]):
        for p in net[1][i][1]:
            print("p%d -> t%d;" % (p, i))
        for p in net[1][i][2]:
            print("t%d -> p%d;" % (i, p))
        i = i + 1
    print("}")
