def exp_tr_cid(tr, sep, ci):
    for act in tr:
        print("%s%s%s" % (ci, sep, act))

def exp_hea(sep, ci, ai):
    print("%s%s%s" % (ci, sep, ai))

def exp_trs(trs, sep, ci, ai):
    exp_hea(sep, ci, ai)
    i = 0
    while i < len(trs):
        if len(trs[i]) == 2 and type(trs[i][1]) is tuple:
            if len(trs[i][0]) > 0:
                exp_tr_cid(trs[i][1], ",", trs[i][0])
            else:
                exp_tr_cid(trs[i][1], ",", str(i))
        else:
            exp_tr_cid(trs[i], ",", str(i))
        i = i + 1
