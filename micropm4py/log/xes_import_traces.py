# RAN ON CORTEX M3, 64kb RAM
def r(tr, p, on, row):
    if on == 2:
        if "concept:name" in row:
            p.append(row.split("value=\"")[1].split("\"")[0])
        elif "</event" in row:
            on = 1
    elif on == 1:
        if "<event" in row:
            on = 2
        elif "</trace" in row:
            tr = p
            p = None
            on = 0
    else:
        tr = None
        if "<trace" in row:
            p = []
            on = 1
    return tr, p, on

if __name__ == "__main__":
    tr = None
    p = None
    on = 0
    tr, p, on = r(tr, p, on, "<?xml version='1.0' encoding='UTF-8'?>")
    tr, p, on = r(tr, p, on, "<log>")
    tr, p, on = r(tr, p, on, "\t<trace>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"C\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t</trace>")
    print(tr)
    tr, p, on = r(tr, p, on, "\t<trace>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"A\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t\t<event>")
    tr, p, on = r(tr, p, on, "\t\t\t<string key=\"concept:name\" value=\"B\" />")
    tr, p, on = r(tr, p, on, "\t\t</event>")
    tr, p, on = r(tr, p, on, "\t</trace>")
    print(tr)
    tr, p, on = r(tr, p, on, "</log>")
