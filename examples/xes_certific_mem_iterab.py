import micropm4py
from micropm4py.log import xes_import_traces_file_standard
from micropm4py.conversion.dfg import dfg_mining
from pympler.asizeof import asizeof
import os


class Shared:
    results = []


def test_log(log_name, log_path):
    print("xes_certific_mem_iterab", log_name)
    dfg = micropm4py.log.xes_import_traces_file_standard.imp_dfg_file_sten(log_path)
    net, im, fm = micropm4py.conversion.dfg.dfg_mining.apply(dfg)
    it = micropm4py.log.xes_import_traces_file_standard.get_it_from_file(log_path)
    nxt = micropm4py.log.xes_import_traces_file_standard.get_nxt_trace(it)
    mp_memory = 16384
    mp4_memory = asizeof(micropm4py)
    net_memory = asizeof(net) + 2*asizeof(im) + 2*asizeof(fm)
    max_it_memory = 0
    while nxt:
        max_it_memory = max(max_it_memory, asizeof(nxt) + asizeof(it))
        nxt = micropm4py.log.xes_import_traces_file_standard.get_nxt_trace(it)
    sum_max_memory = mp_memory + mp4_memory + net_memory + max_it_memory
    Shared.results.append([log_name, max_it_memory, net_memory, mp4_memory, mp_memory, sum_max_memory])


def main():
    for log_name in os.listdir("cert_art"):
        log_path = os.path.join("cert_art", log_name)
        test_log(log_name, log_path)

    for log_name in os.listdir("cert_real"):
        log_path = os.path.join("cert_real", log_name)
        test_log(log_name, log_path)


def save_table(target_html):
    F = open(target_html, "w")
    F.write("<table class=\"table\">\n")
    F.write("<thead>\n")
    F.write("<tr>\n")
    F.write("<th scope=\"col\">Log name</th>")
    F.write("<th scope=\"col\">Max XES iterable size</th>")
    F.write("<th scope=\"col\">DFG mining net size</th>")
    F.write("<th scope=\"col\">MicroPM4Py module size</th>")
    F.write("<th scope=\"col\">MicroPython size (est.max.)</th>\n")
    F.write("<th scope=\"col\">MAX EST. SIZE</th>\n")
    F.write("</tr>\n")
    F.write("</thead>\n")
    F.write("<tbody>\n")
    for row in Shared.results:
        F.write("<tr>\n")
        F.write("<th scope=\"row\">%s</td>" % (row[0]))
        F.write("<td>%d</td>" % (row[1]))
        F.write("<td>%d</td>" % (row[2]))
        F.write("<td>%d</td>" % (row[3]))
        F.write("<td>%d</td>" % (row[4]))
        F.write("<td>%d</td>\n" % (row[5]))
        F.write("</tr>\n")
    F.write("</tbody>\n")
    F.write("</table>\n")
    F.close()


def main2():
    test_log("running-example", "../micro_tests/running-example.xes")
    test_log("receipt", "../../receipt.xes")
    test_log("roadtraffic", "../../roadtraffic.xes")


if __name__ == "__main__":
    main2()
    main()
    save_table("result_iter.html")
    pass