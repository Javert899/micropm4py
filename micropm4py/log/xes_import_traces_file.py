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
    line = F.readline()
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line, d)
        if tr is not None:
            dfg = xes_import_traces.udf_sten(dfg, tr[1])
        line = F.readline()
    F.close()
    dfg[0] = tuple(dfg[0])
    dfg[2] = tuple(dfg[2])
    dfg[3] = tuple(dfg[3])
    return dfg


def get_it_from_file(file_path):
    F = open(file_path, "r")
    it = [0, {}, set(), F]
    return it


def get_nxt_trace(it):
    line = it[3].readline()
    tr = None
    p = None
    while line:
        tr, p, on = xes_import_traces.r(tr, p, it[0], line, {})
        it[0] = on
        if tr is not None:
            return tr
        line = it[3].readline()
    it[3].close()
    return None


def get_nxt_unq_trace(it):
    line = it[3].readline()
    tr = None
    p = None
    while line:
        tr, p, on = xes_import_traces.r(tr, p, it[0], line, it[1])
        it[0] = on
        if tr is not None and not tr[1] in it[2]:
            it[2].add(tr[1])
            return tr
        line = it[3].readline()
    it[3].close()
    return None


def imp_variants_from_file(file_path):
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
                vv[tr[1]] = 0
            vv[tr[1]] = vv[tr[1]] + 1
        line = F.readline()
    F.close()
    return vv
