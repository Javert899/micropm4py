from micropm4py.log import xes_import_traces_file
from micropm4py.discovery import alpha
from micropm4py.visualization import petri_print
from micropm4py.util import copy
from micropm4py.petrinet import petrinet_exec
import time


def main():
    aa = time.ticks_ms()
    log_path = "../micro_tests/running-example.xes"
    dfg = xes_import_traces_file.imp_dfg_file(log_path)
    bb = time.ticks_ms()
    print(bb-aa, "imported DFG")
    net, im, fm = alpha.alpha(dfg)
    cc = time.ticks_ms()
    print(cc-bb, "applied Alpha Miner")
    del dfg
    petri_print.print_dot(net)
    dd = time.ticks_ms()
    print(dd-cc, "performed visualization")
    it = xes_import_traces_file.get_it_from_file(log_path)
    nxt = xes_import_traces_file.get_nxt_trace(it)
    while nxt:
        print(petrinet_exec.ex_trace(net, copy.copy(im), copy.copy(fm), nxt[1]), nxt[1])
        nxt = xes_import_traces_file.get_nxt_trace(it)
    ee = time.ticks_ms()
    print(ee-dd, "performed replay")


if __name__ == "__main__":
    time.ticks_ms = time.time
    main()
