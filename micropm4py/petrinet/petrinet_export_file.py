# Supports only visible transitions, and with arc weight equal to 1. Supports duplicate transitions.
def export(net, im, fm, file_path):
    F = open(file_path, "w")
    F.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    F.write("<pnml>\n")
    F.write("<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">\n")
    F.write("<page id=\"n0\">\n")
    i = 0
    while i < len(net[0]):
        F.write("<place id=\"pl%d\">\n" % (i))
        F.write("<name>\n")
        F.write("<text>%s</text>\n" % (net[0][i]))
        F.write("</name>\n")
        if i in im:
            F.write("<initialMarking>\n")
            F.write("<text>%d</text>\n" % (im[i]))
            F.write("</initialMarking>\n")
        F.write("</place>\n")
        i = i + 1
    a = 0
    i = 0
    while i < len(net[1]):
        F.write("<transition id=\"tr" + str(i) + "\">\n")
        F.write("<name>\n")
        F.write("<text>" + net[1][i][0] + "</text>\n")
        F.write("</name>\n")
        F.write("</transition>\n")
        for p in net[1][i][1]:
            a = a + 1
            F.write("<arc id=\"ac%d\" source=\"pl%d\" target=\"tr%d\"/>\n" % (a, p, i))
        for p in net[1][i][2]:
            a = a + 1
            F.write("<arc id=\"ac%d\" source=\"tr%d\" target=\"pl%d\"/>\n" % (a, i, p))
        i = i + 1
    F.write("</page>\n")
    F.write("<finalmarkings>\n")
    F.write("<marking>\n")
    for p in fm:
        F.write("<place idref=\"pl%d\">\n" % (p))
        F.write("<text>%d</text>\n" % (fm[p]))
        F.write("</place>\n")
    F.write("</marking>\n")
    F.write("</finalmarkings>\n")
    F.write("</net>\n")
    F.write("</pnml>\n")
    F.close()
