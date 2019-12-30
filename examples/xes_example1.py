from micropm4py.log import xes_import_traces_file_standard
from micropm4py.log import xes_export_traces_file
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.visualization import dfg_print
import os


def main():
    log = xes_import_traces_file_standard.imp_list_traces_from_file("../micro_tests/running-example.xes")
    print(log)
    xes_export_traces_file.export_traces(log, "ru.xes")
    os.remove("ru.xes")
    dfg = traces_to_dfg.trs_to_dfg(log)
    # print the DOT (that can be layouted easily with the command line)
    dfg_print.prnt_dot(dfg)


if __name__ == "__main__":
    main()
