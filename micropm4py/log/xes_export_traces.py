def st_exp():
    print("<?xml version='1.0' encoding='UTF-8'?>")
    print("<log>")


def exp_tr_cid(tr, cid):
    print("\t<trace>")
    print("\t\t<string key=\"concept:name\" value=\"%s\" />" % (cid))
    for act in tr:
        print("\t\t<event>")
        print("\t\t\t<string key=\"concept:name\" value=\"%s\" />" % (act))
        print("\t\t</event>")
    print("\t</trace>")


def exp_tr(tr):
    print("\t<trace>")
    for act in tr:
        print("\t\t<event>")
        print("\t\t\t<string key=\"concept:name\" value=\"%s\" />" % (act))
        print("\t\t</event>")
    print("\t</trace>")


def end_exp():
    print("</log>")
