from micropm4py.log import xes_import_traces_file_standard
from micropm4py.petrinet import petrinet_import_file
from micropm4py.util import copy
from micropm4py.petrinet import petrinet_exec


def main():
    log = xes_import_traces_file_standard.imp_list_traces_from_file("../micro_tests/running-example.xes")
    net, im, fm = petrinet_import_file.imp_file("../micro_tests/running-example.pnml")
    for tr in log:
        print(tr[1], petrinet_exec.ex_trace(net, copy.copy(im), copy.copy(fm), tr[1]))


if __name__ == "__main__":
    main()
