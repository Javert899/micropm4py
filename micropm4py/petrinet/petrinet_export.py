# supports only visible transitions, and with arc weight equal to 1
def export(net, im, fm):
    print("<?xml version='1.0' encoding='UTF-8'?>")
    print("<pnml>")
    print("<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">")
    print("<page id=\"n0\">")
    i = 0
    while i < len(net[0]):
        print("<place id=\""+net[0][i]+"\">")
        print("<name>")
        print("<text>"+net[0][i]+"</text>")
        print("</name>")
        if i in im:
            print("<initialMarking>")
            print("<text>"+str(im[i])+"</text>")
            print("</initialMarking>")
        print("</place>")
        i = i + 1
    a = 0
    i = 0
    while i < len(net[1]):
        print("<transition id=\""+net[1][i][0]+"\">")
        print("<name>")
        print("<text>"+net[1][i][0]+"</text>")
        print("</name>")
        print("</transition>")
        for p in net[1][i][1]:
            a = a + 1
            print("<arc id=\"ac"+str(a)+"\" source=\""+net[0][p]+"\" target=\""+net[1][i][0]+"\"/>")
        for p in net[1][i][2]:
            a = a + 1
            print("<arc id=\"ac"+str(a)+"\" source=\""+net[1][i][0]+"\" target=\""+net[0][p]+"\"/>")
        i = i + 1
    print("</page>")
    print("<finalmarkings>")
    print("<marking>")
    for p in fm:
        print("<place idref=\""+net[0][p]+"\">")
        print("<text>1</text>")
        print("</place>")
    print("</marking>")
    print("</finalmarkings>")
    print("</net>")
    print("</pnml>")

if __name__ == "__main__":
    p = [["source", "p1", "sink"], [["A", {0: 1}, {1: 1}], ["B", {1: 1}, {2: 1}]]]
    export(p, {0: 1}, {2: 1})
