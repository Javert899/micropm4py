from micropm4py.log import xes_import_traces


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
