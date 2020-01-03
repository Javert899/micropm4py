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


def frm(net, im, fm):
    net0 = [[], []]
    im0 = {}
    fm0 = {}
    places = list(net.places)
    transitions = list(net.transitions)
    dp = {places[i]:i for i in range(len(places))}
    for p in places:
        net0[0].append(p.name)
    for t in transitions:
        net0[1].append([t.label, [], []])
        for a in t.in_arcs:
            p = a.source
            #w = a.weight
            net0[1][-1][1].append(dp[p])
        for a in t.out_arcs:
            p = a.target
            #w = a.weight
            net0[1][-1][2].append(dp[p])
    for p in im:
        im0[dp[p]] = im[p]
    for p in fm:
        fm0[dp[p]] = fm[p]
    net0[0] = tuple(net0[0])
    i = 0
    while i < len(net0[1]):
        net0[1][i][1] = tuple(net0[1][i][1])
        net0[1][i][2] = tuple(net0[1][i][2])
        net0[1][i] = tuple(net0[1][i])
        i = i + 1
    net0[1] = tuple(net0[1])
    return net0, im0, fm0
