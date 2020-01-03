from micropm4py.log import xes_import_traces_file_standard
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.visualization.dfg_saver import save_dot
from micropm4py.log import xes_export_traces_file
import os


def test_log(log_name, log_path):
    print("doing",log_name)
    log = xes_import_traces_file_standard.imp_list_traces_from_file(log_path)
    log_export_path = os.path.join("cert_res", log_name.replace(".xes", "_export.xes"))
    xes_export_traces_file.export_traces(log, log_export_path)
    log_print_path = os.path.join("cert_res", log_name.replace("xes", "txt"))
    F = open(log_print_path, "w")
    for trace in log:
        F.write("%s %s\n" % (trace[0], str(trace[1])))
    F.close()
    dfg = traces_to_dfg.trs_to_dfg(log)
    dot_path = os.path.join("cert_res", log_name.replace("xes", "dot"))
    save_dot(dot_path, dfg)
    print("done",log_name)


def main():
    for log_name in os.listdir("cert_art"):
        log_path = os.path.join("cert_art", log_name)
        test_log(log_name, log_path)

    for log_name in os.listdir("cert_real"):
        log_path = os.path.join("cert_real", log_name)
        test_log(log_name, log_path)


if __name__ == "__main__":
    main()
