from micropm4py.log import xes_import_traces_file_standard
from micropm4py.log import postprocessing
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.conversion.dfg import dfg_mining
from micropm4py.visualization import petri_saver
from micropm4py.util import copy
from micropm4py.petrinet import petrinet_exec


def main():
    log = xes_import_traces_file_standard.imp_list_traces_from_file("../micro_tests/running-example.xes")
    log = postprocessing.add_art_st_end(log)
    dfg = traces_to_dfg.trs_to_dfg(log)
    net, im, fm = dfg_mining.apply(dfg)
    #petri_saver.save_dot("ru_dm.dot", net)
    for tr in log:
        print(tr[1], petrinet_exec.ex_trace(net, copy.copy(im), copy.copy(fm), tr[1]))


if __name__ == "__main__":
    main()
