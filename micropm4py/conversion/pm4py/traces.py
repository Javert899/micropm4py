import pm4py


def to_trace(list_act, cid):
    t = pm4py.objects.log.log.Trace()
    t.attributes["concept:name"] = cid
    for act in list_act:
        t.append(pm4py.objects.log.log.Event({"concept:name": act}))
    return t


def to(trs):
    l = pm4py.objects.log.log.EventLog()
    i = 0
    while i < len(trs):
        if len(trs[i]) == 2 and type(trs[i][1]) is list:
            if len(trs[i][0]) > 0:
                t = to_trace(trs[i][1], trs[i][0])
            else:
                t = to_trace(trs[i][1], str(i))
        else:
            t = to_trace(trs[i], str(i))
        l.append(t)
        i = i + 1
    return l
