import pm4py
from micropm4py.log import xes_import_traces_file
from micropm4py.conversion.pm4py import traces


def main():
    log0 = xes_import_traces_file.imp_list_traces_from_file("../micro_tests/running-example.xes")
    print(log0)
    log = traces.to(log0)
    print(log)
    log1 = traces.frm(log)
    print(log1)


if __name__ == "__main__":
    main()
