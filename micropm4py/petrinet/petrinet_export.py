def export(net, im, fm):
    print("<?xml version='1.0' encoding='UTF-8'?>")
    print("<pnml>")
    print("<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">")
    print("<page id=\"n0\">")
    i = 0
    while i < len(net[0]):
        print("<place id=\"pl%d\">" % (i))
        print("<name>")
        print("<text>%s</text>" % (i))
        print("</name>")
        if i in im:
            print("<initialMarking>")
            print("<text>%d</text>" % (im[i]))
            print("</initialMarking>")
        print("</place>")
        i = i + 1
    a = 0
    i = 0
    while i < len(net[1]):
        print("<transition id=\"tr%d\">" % (i))
        print("<name>")
        print("<text>%s</text>" % (net[1][i][0]))
        print("</name>")
        print("</transition>")
        for p in net[1][i][1]:
            a = a + 1
            print("<arc id=\"ac%d\" source=\"pl%d\" target=\"tr%d\"/>" % (a, p, i))
        for p in net[1][i][2]:
            a = a + 1
            print("<arc id=\"ac%d\" source=\"tr%d\" target=\"pl%d\"/>" % (a, i, p))
        i = i + 1
    print("</page>")
    print("<finalmarkings>")
    print("<marking>")
    for p in fm:
        print("<place idref=\"pl%d\">" % (p))
        print("<text>%d</text>" % (fm[p]))
        print("</place>")
    print("</marking>")
    print("</finalmarkings>")
    print("</net>")
    print("</pnml>")
