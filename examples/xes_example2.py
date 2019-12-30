from micropm4py.log import xes_import_traces_file_standard
from micropm4py.visualization import dfg_print


def main():
    # import the DFG directly from the XES (no artificial start/end activities)
    dfg = xes_import_traces_file_standard.imp_dfg_file("../micro_tests/running-example.xes")
    print(dfg)
    dfg_print.prnt_dot(dfg)
    # import the DFG directly from the XES (artificial start/end activities)
    dfg = xes_import_traces_file_standard.imp_dfg_file_sten("../micro_tests/running-example.xes")
    print(dfg)
    dfg_print.prnt_dot(dfg)


if __name__ == "__main__":
    main()
