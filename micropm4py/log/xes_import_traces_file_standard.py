from micropm4py.log import xes_import_traces


def get_line(F):
    by = F.read(1)
    line = ""
    while by:
        if by == "\r" or by == "\n":
            by = F.read(1)
            continue
        line = line + by
        if by == ">":
            return line
        by = F.read(1)


def imp_list_traces_from_file(file_path):
    list_traces = []
    tr = None
    p = None
    on = 0
    d = {}
    vv = {}
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            if tr[1] not in vv:
                vv[tr[1]] = tr[1]
            tr[1] = vv[tr[1]]
            list_traces.append(tuple(tr))
        line = get_line(F)
    F.close()
    return list_traces


def imp_dfg_file(file_path):
    dfg = [[], dict(), set(), set(), dict()]
    tr = None
    p = None
    on = 0
    d = {}
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            dfg = xes_import_traces.udf(dfg, tr[1])
        line = get_line(F)
    F.close()
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    return dfg


def imp_dfg_file_sten(file_path):
    dfg = [[], dict(), set(), set(), dict()]
    tr = None
    p = None
    on = 0
    d = {}
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            dfg = xes_import_traces.udf_sten(dfg, tr[1])
        line = get_line(F)
    F.close()
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    return dfg
