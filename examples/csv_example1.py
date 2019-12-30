from micropm4py.log import csv_import_traces_file, csv_export_traces_file
from micropm4py.log import xes_export_traces_file
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.visualization import dfg_print
import os


def main():
    # import the CSV. Arguments:
    # 1) path of the CSV file
    # 2) separator
    # 3) column that hosts the case ID
    # 4) column that hosts the activity
    log = csv_import_traces_file.import_traces_path("../micro_tests/running-example.csv", ",", "case:concept:name", "concept:name")
    print(log)
    # export the CSV. Arguments:
    # 1) path of the exported CSV file
    # 2) separator
    # 3) column that hosts the case ID
    # 4) column that hosts the activity
    csv_export_traces_file.export_to_path(log, "ru.csv", ",", "case:concept:name", "concept:name")
    os.remove("ru.csv")
    xes_export_traces_file.export_traces(log, "ru.xes")
    os.remove("ru.xes")
    dfg = traces_to_dfg.trs_to_dfg(log)
    # print the DOT (that can be layouted easily with the command line)
    dfg_print.prnt_dot(dfg)


if __name__ == "__main__":
    main()
