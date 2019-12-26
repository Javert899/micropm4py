from micropm4py.log import csv_import_traces


def import_traces_path(file_path, sep, ci, ai):
    F = open(file_path, "r")
    line = F.readline()
    cidp, acp = csv_import_traces.import_header(line, sep, ci, ai)
    d = {}
    line = F.readline()
    while line:
        d = csv_import_traces.import_traces(d, line, sep, cidp, acp)
        line = F.readline()
    F.close()
    d = csv_import_traces.finish_traces(d)
    return d


def import_dfg_path(file_path, sep, ci, ai):
    F = open(file_path, "r")
    line = F.readline()
    cidp, acp = csv_import_traces.import_header(line, sep, ci, ai)
    dfg = [[], dict(), set(), set(), dict()]
    d = {}
    line = F.readline()
    while line:
        dfg, d = csv_import_traces.import_dfg(dfg, d, line, sep, cidp, acp)
        line = F.readline()
    F.close()
    dfg = csv_import_traces.finish_dfg(dfg, d)
    return dfg
