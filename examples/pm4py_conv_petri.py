import pm4py
from micropm4py.petrinet import petrinet_import_file
from micropm4py.conversion.pm4py import petri


def main():
    net0, im0, fm0 = petrinet_import_file.imp_file("../micro_tests/running-example.pnml")
    print(net0)
    print(im0)
    print(fm0)
    net, im, fm = petri.to(net0, im0, fm0)
    print("")
    print(net.places)
    print(net.transitions)
    net1, im1, fm1 = petri.frm(net, im, fm)
    print("")
    print(net1)
    print(im1)
    print(fm1)


if __name__ == "__main__":
    main()
