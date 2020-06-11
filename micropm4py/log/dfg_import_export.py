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
        dfg[2].append(line.split("x")[0])
        line = F.readline().strip()
    no = int(line)
    line = F.readline().strip()
    for i in range(no):
        dfg[3].append(line.split("x")[0])
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
