from micropm4py.log import xes_import_traces


def imp_dfg_file(file_path):
    dfg = [[], dict(), set(), set(), dict()]
    tr = None
    p = None
    on = 0
    d = {}
    F = open(file_path, "r")
    line = F.readline()
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            dfg = xes_import_traces.udf(dfg, tr[1])
        line = F.readline()
    F.close()
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    dfg = tuple(dfg)
    return dfg
