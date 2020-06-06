from micropm4py.log import xes_import_traces_file
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.discovery import alpha
from micropm4py.petrinet import alignments
import time
import os


def main():
    log = xes_import_traces_file.imp_list_traces_from_file(os.path.join("..", "micro_tests", "running-example.xes"))
    #log = xes_import_traces_file.imp_list_traces_from_file("C:/reviewing.xes")
    dfg = traces_to_dfg.trs_to_dfg(log)
    net, im, fm = alpha.alpha(dfg)
    aa = time.time()
    i = 0
    while i < len(log):
        align = alignments.apply(log[i], net, im, fm, ret_tuple_as_trans_desc=False)
        print(align)
        i = i + 1
    bb = time.time()
    print(bb - aa)


if __name__ == "__main__":
    time.ticks_ms = time.time
    main()
