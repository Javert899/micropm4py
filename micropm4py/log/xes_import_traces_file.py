from micropm4py.log import xes_import_traces


def imp_list_traces_from_file(file_path):
    list_traces = []
    tr = None
    p = None
    vv = {}
    on = 0
    d = {}
    F = open(file_path, "r")
    line = F.readline()
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            if tr[1] not in vv:
                vv[tr[1]] = tr[1]
            tr[1] = vv[tr[1]]
            list_traces.append(tuple(tr))
        line = F.readline()
    F.close()
    return list_traces


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
    return dfg


def imp_dfg_file_sten(file_path):
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
            dfg = xes_import_traces.udf_sten(dfg, tr[1])
        line = F.readline()
    F.close()
    return dfg
