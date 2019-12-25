# RAN ON CORTEX M3, 64kb RAM
def st_exp():
    print("<?xml version='1.0' encoding='UTF-8'?>")
    print("<log>")


def exp_tr_cid(tr, cid):
    print("\t<trace>")
    print("\t\t<string key=\"concept:name\" value=\"" + str(cid) + "\" />")
    for act in tr:
        print("\t\t<event>")
        print("\t\t\t<string key=\"concept:name\" value=\"" + act + "\" />")
        print("\t\t</event>")
    print("\t</trace>")


def exp_tr(tr):
    print("\t<trace>")
    for act in tr:
        print("\t\t<event>")
        print("\t\t\t<string key=\"concept:name\" value=\"" + act + "\" />")
        print("\t\t</event>")
    print("\t</trace>")


def end_exp():
    print("</log>")


def main():
    st_exp()
    exp_tr_cid(["A", "B", "C"], "case1")
    exp_tr(["A", "B"])
    end_exp()


if __name__ == "__main__":
    main()
