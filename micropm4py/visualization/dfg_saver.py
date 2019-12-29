def save_dot(file_path, dfg):
    F = open(file_path, "w")
    F.write("digraph graphname {\n")
    i = 0
    while i < len(dfg[0]):
        F.write("%d [label=\"%s (%d)\"];\n" % (i, dfg[0][i], dfg[1][i]))
        i = i + 1
    for tup in dfg[4]:
        F.write("%d -> %d [label=\"%d\"];\n" % (tup[0], tup[1], dfg[4][tup]))
    F.write("}\n")
    F.close()
