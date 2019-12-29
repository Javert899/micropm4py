def save_dot(file_path, net):
    F = open(file_path, "w")
    F.write("digraph graphname {\n")
    i = 0
    while i < len(net[0]):
        F.write("p%d [label=\"\"];\n" % (i,))
        i = i + 1
    i = 0
    while i < len(net[1]):
        F.write("t%d [label=\"%s\", shape=box];\n" % (i, net[1][i][0]))
        i = i + 1
    i = 0
    while i < len(net[1]):
        for p in net[1][i][1]:
            F.write("p%d -> t%d;\n" % (p, i))
        for p in net[1][i][2]:
            F.write("t%d -> p%d;\n" % (i, p))
        i = i + 1
    F.write("}\n")
    F.close()
