from micropm4py.log import csv_import_traces_file
from micropm4py.visualization import dfg_print


def main():
    # import the DFG directly from the CSV (no artificial start/end activities). Arguments:
    # 1) path of the CSV file
    # 2) separator
    # 3) column that hosts the case ID
    # 4) column that hosts the activity
    dfg = csv_import_traces_file.import_dfg_path("../micro_tests/running-example.csv", ",", "case:concept:name", "concept:name")
    print(dfg)
    # print the DOT (that can be layouted easily with the command line)
    dfg_print.prnt_dot(dfg)
    # import the DFG directly from the CSV (with artificial start/end activities). Arguments:
    # 1) path of the CSV file
    # 2) separator
    # 3) column that hosts the case ID
    # 4) column that hosts the activity
    dfg = csv_import_traces_file.import_dfg_path_sten("../micro_tests/running-example.csv", ",", "case:concept:name", "concept:name")
    print(dfg)
    # print the DOT (that can be layouted easily with the command line)
    dfg_print.prnt_dot(dfg)


if __name__ == "__main__":
    main()
