def st_exp(F):
    F.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    F.write("<log>\n")


def exp_tr_cid(F, tr, cid):
    F.write("\t<trace>\n")
    F.write("\t\t<string key=\"concept:name\" value=\"%s\" />\n" % (cid))
    for act in tr:
        F.write("\t\t<event>\n")
        F.write("\t\t\t<string key=\"concept:name\" value=\"%s\" />\n" % (act))
        F.write("\t\t</event>\n")
    F.write("\t</trace>\n")


def exp_tr(F, tr):
    F.write("\t<trace>\n")
    for act in tr:
        F.write("\t\t<event>\n")
        F.write("\t\t\t<string key=\"concept:name\" value=\"%s\" />\n" % (act))
        F.write("\t\t</event>\n")
    F.write("\t</trace>\n")


def end_exp(F):
    F.write("</log>\n")


def export_traces(list_traces, file_path):
    F = open(file_path, "w")
    st_exp(F)
    for tr in list_traces:
        if len(tr) == 2 and type(tr[1]) is list:
            if len(tr[0]) > 0:
                exp_tr_cid(F, tr[1], tr[0])
            else:
                exp_tr(F, tr[1])
        else:
            exp_tr(F, tr)
    end_exp(F)
    F.close()
