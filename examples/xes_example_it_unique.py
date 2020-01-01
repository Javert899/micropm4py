from micropm4py.log import xes_import_traces_file_standard


def main():
    # load the trace from the XES file one-by-one, avoiding loading the entire log in memory :)
    # in this case, the next *unique* trace is retrieved, that means only one trace per variant is reported
    it = xes_import_traces_file_standard.get_it_from_file("../micro_tests/running-example.xes")
    nxt = xes_import_traces_file_standard.get_nxt_unq_trace(it)
    while nxt:
        print(nxt)
        nxt = xes_import_traces_file_standard.get_nxt_unq_trace(it)


if __name__ == "__main__":
    main()
