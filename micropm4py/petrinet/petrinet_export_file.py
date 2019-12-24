def export(net, im, fm, file_path):
    F = open(file_path, "w")
    F.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    F.write("<pnml>\n")
    F.write("<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">\n")
    F.write("<page id=\"n0\">\n")
    i = 0
    while i < len(net[0]):
        F.write("<place id=\""+net[0][i]+"\">\n")
        F.write("<name>\n")
        F.write("<text>"+net[0][i]+"</text>\n")
        F.write("</name>\n")
        if i in im:
            F.write("<initialMarking>\n")
            F.write("<text>"+str(im[i])+"</text>\n")
            F.write("</initialMarking>\n")
        F.write("</place>\n")
        i = i + 1
    a = 0
    i = 0
    while i < len(net[1]):
        F.write("<transition id=\""+net[1][i][0]+"\">\n")
        F.write("<name>\n")
        F.write("<text>"+net[1][i][0]+"</text>\n")
        F.write("</name>\n")
        F.write("</transition>\n")
        for p in net[1][i][1]:
            a = a + 1
            F.write("<arc id=\"ac"+str(a)+"\" source=\""+net[0][p]+"\" target=\""+net[1][i][0]+"\"/>\n")
        for p in net[1][i][2]:
            a = a + 1
            F.write("<arc id=\"ac"+str(a)+"\" source=\""+net[1][i][0]+"\" target=\""+net[0][p]+"\"/>\n")
        i = i + 1
    F.write("</page>\n")
    F.write("<finalmarkings>\n")
    F.write("<marking>\n")
    for p in fm:
        F.write("<place idref=\""+net[0][p]+"\">\n")
        F.write("<text>1</text>\n")
        F.write("</place>\n")
    F.write("</marking>\n")
    F.write("</finalmarkings>\n")
    F.write("</net>\n")
    F.write("</pnml>\n")
    F.close()
