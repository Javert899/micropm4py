import pm4py.objects.log.log as pm4py_log


def to_trace(list_act, cid):
    t = pm4py_log.Trace()
    t.attributes["concept:name"] = cid
    for act in list_act:
        t.append(pm4py_log.Event({"concept:name": act}))
    return t


def to(trs):
    l = pm4py_log.EventLog()
    i = 0
    while i < len(trs):
        if len(trs[i]) == 2 and type(trs[i][1]) is tuple:
            if len(trs[i][0]) > 0:
                t = to_trace(trs[i][1], trs[i][0])
            else:
                t = to_trace(trs[i][1], str(i))
        else:
            t = to_trace(trs[i], str(i))
        l.append(t)
        i = i + 1
    return l


def frm(log):
    trs = []
    i = 0
    while i < len(log):
        if "concept:name" in log[i].attributes:
            cid = log[i].attributes["concept:name"]
        else:
            cid = str(i)
        list_act = []
        for eve in log[i]:
            list_act.append(eve["concept:name"])
        trs.append((cid, tuple(list_act)))
        i = i + 1
    return trs
