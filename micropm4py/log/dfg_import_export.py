def import_dfg(file_path):
    F = open(file_path, "r")
    dfg = [[], {}, [], [], {}]
    line = F.readline().strip()
    no = int(line)
    line = F.readline().strip()
    for i in range(no):
        dfg[0].append(line)
        dfg[1][len(dfg[1])] = 1
        line = F.readline().strip()
    no = int(line)
    line = F.readline().strip()
    for i in range(no):
        dfg[2].append(int(line.split("x")[0]))
        line = F.readline().strip()
    no = int(line)
    line = F.readline().strip()
    for i in range(no):
        dfg[3].append(int(line.split("x")[0]))
        line = F.readline().strip()
    while line:
        line = line.strip()
        if line:
            line = line.split("x")
            dfg[4][(int(line[0].split(">")[0]), int(line[0].split(">")[1]))] = int(line[1])
        line = F.readline()
    F.close()
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    dfg = tuple(dfg)
    return dfg


def print_dfg(dfg):
    print("%d" % (len(dfg[0])))
    for a in dfg[0]:
        print("%s" % (a))
    print("%d" % len(dfg[2]))
    for a in dfg[2]:
        print("%dx1" % (a))
    print("%d" % (len(dfg[3])))
    for a in dfg[3]:
        print("%dx1" % (a))
    for (a1, a2) in dfg[4]:
        print("%d>%dx%d" % (a1, a2, dfg[4][(a1, a2)]))


def export_dfg_file(dfg, file_path):
    F = open(file_path, "w")
    F.write("%d\n" % (len(dfg[0])))
    for a in dfg[0]:
        F.write("%s\n" % (a))
    F.write("%d\n" % len(dfg[2]))
    for a in dfg[2]:
        F.write("%dx1\n" % (a))
    F.write("%d\n" % (len(dfg[3])))
    for a in dfg[3]:
        F.write("%dx1\n" % (a))
    for (a1, a2) in dfg[4]:
        F.write("%d>%dx%d\n" % (a1, a2, dfg[4][(a1, a2)]))
    F.close()
