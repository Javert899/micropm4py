from micropm4py.log import xes_import_traces

def imp_file(file_path):
    list_traces = []
    tr = None
    p = None
    on = 0
    F = open(file_path, "r")
    line = F.readline()
    while line:
        tr, p, on = xes_import_traces.r(tr, p, on, line)
        if tr is not None:
            list_traces.append(tr)
        line = F.readline()
    F.close()
    return list_traces
