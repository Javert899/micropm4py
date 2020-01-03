import micropm4py
from pympler.asizeof import asizeof
import os


class Shared:
    results = []


def test_log(log_name, log_path):
    log = micropm4py.log.xes_import_traces_file_standard.imp_list_traces_from_file(log_path)
    dfg = micropm4py.log.xes_import_traces_file_standard.imp_dfg_file(log_path)
    variants = micropm4py.log.xes_import_traces_file_standard.imp_variants_from_file(log_path)
    Shared.results.append([log_name, asizeof(dfg), asizeof(variants), asizeof(log)])


def main():
    for log_name in os.listdir("cert_art"):
        log_path = os.path.join("cert_art", log_name)
        test_log(log_name, log_path)

    for log_name in os.listdir("cert_real"):
        log_path = os.path.join("cert_real", log_name)
        test_log(log_name, log_path)


def main2():
    test_log("running-example", "../micro_tests/running-example.xes")
    test_log("receipt", "../../receipt.xes")


def save_table(target_html):
    F = open(target_html, "w")
    F.write("<table class=\"table\">\n")
    F.write("<thead>\n")
    F.write("<tr>\n")
    F.write("<th scope=\"col\">Log name</th>")
    F.write("<th>DFG obj size</th>")
    F.write("<th>Variants obj size</th>")
    F.write("<th>Loaded log obj size</th>")
    F.write("</tr>\n")
    F.write("</thead>\n")
    F.write("<tbody>\n")
    for row in Shared.results:
        F.write("<tr>\n")
        F.write("<th scope=\"row\">%s</td>" % (row[0]))
        F.write("<td>%d</td>" % (row[1]))
        F.write("<td>%d</td>" % (row[2]))
        F.write("<td>%d</td>" % (row[3]))
        F.write("</tr>\n")
    F.write("</tbody>\n")
    F.write("</table>\n")
    F.close()


if __name__ == "__main__":
    #main2()
    #main()
    #save_table("results_iter.html")
    pass
