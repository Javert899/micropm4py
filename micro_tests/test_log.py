from micropm4py.log import xes_import_traces, xes_export_traces, xes_import_traces_file, xes_export_traces_file
from micropm4py.petrinet import petrinet_import_file, petrinet_exec
import unittest
import os


class TestLog(unittest.TestCase):
    def test_log_import(self):
        xes_import_traces.main()

    def test_log_export(self):
        xes_export_traces.main()

    def test_xes_dfg_import(self):
        dfg = xes_import_traces_file.imp_dfg_file("running-example.xes")

    def test_xes_import_export_file(self):
        log = xes_import_traces_file.imp_list_traces_from_file("running-example.xes")
        xes_export_traces_file.export_traces(log, "ru.xes")
        log = xes_import_traces_file.imp_list_traces_from_file("ru.xes")
        xes_export_traces_file.export_traces(log, "ru2.xes")
        os.remove("ru.xes")
        os.remove("ru2.xes")

    def test_xes_petri_replay(self):
        log = xes_import_traces_file.imp_list_traces_from_file("running-example.xes")
        net, im, fm = petrinet_import_file.imp_file("running-example.pnml")
        r = petrinet_exec.ex_trace(net, im, fm, log[0][1])
        print(r)

if __name__ == "__main__":
    unittest.main()
