from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri.utils import petri as petri_utils

def to(net0, im0, fm0):
    net = PetriNet("")
    im = Marking()
    fm = Marking()
    dp = {}
    dt = {}
    i = 0
    while i < len(net0[0]):
        p = PetriNet.Place(net0[0][i])
        net.places.add(p)
        dp[i] = p
        i = i + 1
    i = 0
    while i < len(net0[1]):
        t = PetriNet.Transition("t%d" % (i), net0[1][i][0])
        net.transitions.add(t)
        dt[i] = t
        i = i + 1
    i = 0
    while i < len(net0[1]):
        for p in net0[1][i][1]:
            petri_utils.utils.add_arc_from_to(dp[p], dt[i], net)
        for p in net0[1][i][2]:
            petri_utils.utils.add_arc_from_to(dt[i], dp[p], net)
        i = i + 1
    for p in im0:
        im[dp[p]] = im0[p]
    for p in fm0:
        fm[dp[p]] = fm0[p]
    return net, im, fm
