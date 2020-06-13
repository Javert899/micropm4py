from micropm4py.log import xes_import_traces_file
from micropm4py.discovery import alpha
from micropm4py.petrinet import alignments
import time
import os


def main():
    log_file = os.path.join("..", "micro_tests", "reviewing.xes")
    dfg = xes_import_traces_file.imp_dfg_file(log_file)
    net, im, fm = alpha.alpha(dfg)
    del dfg
    it = xes_import_traces_file.get_it_from_file(log_file)
    nxt = xes_import_traces_file.get_nxt_trace(it)
    aa = time.ticks_ms()
    while nxt:
        try:
            align = alignments.apply(nxt, net, im, fm, ret_tuple_as_trans_desc=False, enable_gc=True)
            print(align)
        except:
            print("MemoryError")
        nxt = xes_import_traces_file.get_nxt_trace(it)
    bb = time.ticks_ms()
    print(bb - aa)


if __name__ == "__main__":
    time.ticks_ms = time.time
    main()
