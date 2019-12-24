def st_exp(F):
    F.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    F.write("<log>\n")

def exp_tr(F, tr):
    F.write("\t<trace>\n")
    for act in tr:
        F.write("\t\t<event>\n")
        F.write("\t\t\t<string key=\"concept:name\" value=\""+act+"\" />\n")
        F.write("\t\t</event>\n")
    F.write("\t</trace>\n")

def end_exp(F):
    F.write("</log>\n")

def export_traces(list_traces, file_path):
    F = open(file_path, "w")
    st_exp(F)
    for tr in list_traces:
        exp_tr(F, tr)
    end_exp(F)
    F.close()