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
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line)
        if tr is not None:
            list_traces.append(tr)
        line = get_line(F)
    F.close()
    return list_traces


def imp_dfg_file(file_path):
    dfg = [[], dict(), set(), set(), dict()]
    tr = None
    p = None
    on = 0
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line)
        if tr is not None:
            dfg = xes_import_traces.udf(dfg, tr[1])
        line = get_line(F)
    F.close()
    return dfg


def imp_dfg_file_sten(file_path):
    dfg = [[], dict(), set(), set(), dict()]
    tr = None
    p = None
    on = 0
    F = open(file_path, "r")
    line = get_line(F)
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line)
        if tr is not None:
            dfg = xes_import_traces.udf_sten(dfg, tr[1])
        line = get_line(F)
    F.close()
    return dfg
