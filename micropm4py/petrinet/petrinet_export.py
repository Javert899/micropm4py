# RAN ON CORTEX M3, 64kb RAM
# Supports only visible transitions, and with arc weight equal to 1. Supports duplicate transitions.
def export(net, im, fm):
    print("<?xml version='1.0' encoding='UTF-8'?>")
    print("<pnml>")
    print("<net id=\"net1\" type=\"http://www.pnml.org/version-2009/grammar/pnmlcoremodel\">")
    print("<page id=\"n0\">")
    i = 0
    while i < len(net[0]):
        print("<place id=\"pl"+str(i)+"\">")
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
        print("<transition id=\"tr"+str(i)+"\">")
        print("<name>")
        print("<text>"+net[1][i][0]+"</text>")
        print("</name>")
        print("</transition>")
        for p in net[1][i][1]:
            a = a + 1
            print("<arc id=\"ac"+str(a)+"\" source=\"pl"+str(p)+"\" target=\"tr"+str(i)+"\"/>")
        for p in net[1][i][2]:
            a = a + 1
            print("<arc id=\"ac"+str(a)+"\" source=\"tr"+str(i)+"\" target=\"pl"+str(p)+"\"/>")
        i = i + 1
    print("</page>")
    print("<finalmarkings>")
    print("<marking>")
    for p in fm:
        print("<place idref=\"pl"+str(p)+"\">")
        print("<text>1</text>")
        print("</place>")
    print("</marking>")
    print("</finalmarkings>")
    print("</net>")
    print("</pnml>")

if __name__ == "__main__":
    p = [["source", "p1", "sink"], [["A", {0: 1}, {1: 1}], ["B", {1: 1}, {2: 1}]]]
    export(p, {0: 1}, {2: 1})
