def exp_tr_cid(F, tr, sep, ci):
    for act in tr:
        F.write("%s%s%s\n" % (ci, sep, act))

def exp_hea(F, sep, ci, ai):
    F.write("%s%s%s\n" % (ci, sep, ai))

def exp_trs(F, trs, sep, ci, ai):
    exp_hea(F, sep, ci, ai)
    i = 0
    while i < len(trs):
        if len(trs[i]) == 2 and type(trs[i][1]) is list:
            if len(trs[i][0]) > 0:
                exp_tr_cid(F, trs[i][1], ",", trs[i][0])
            else:
                exp_tr_cid(F, trs[i][1], ",", str(i))
        else:
            exp_tr_cid(F, trs[i], ",", str(i))
        i = i + 1

def export_to_path(trs, path, sep, ci, ai):
    F = open(path, "w")
    exp_trs(F, trs, sep, ci, ai)
    F.close()
