from micropm4py.log import xes_import_traces, xes_export_traces, xes_import_traces_file, xes_export_traces_file
from micropm4py.log import csv_import_traces, csv_export_traces
from micropm4py.log import csv_import_traces_file, csv_export_traces_file
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

    def test_xes_dfg_import_sten(self):
        dfg = xes_import_traces_file.imp_dfg_file_sten("running-example.xes")

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

    def test_csv_import(self):
        csv_import_traces.main()
        csv_import_traces.main2()
        csv_import_traces.main3()

    def test_csv_export(self):
        csv_export_traces.main()

    def test_csv_import_file(self):
        log = csv_import_traces_file.import_traces_path("running-example.csv", ",", "case:concept:name", "concept:name")
        dfg = csv_import_traces_file.import_dfg_path("running-example.csv", ",", "case:concept:name", "concept:name")
        xes_export_traces_file.export_traces(log, "ru.xes")
        os.remove("ru.xes")

    def test_csv_import_file_sten(self):
        dfg = csv_import_traces_file.import_dfg_path_sten("running-example.csv", ",", "case:concept:name", "concept:name")

    def test_csv_export_file(self):
        log = xes_import_traces_file.imp_list_traces_from_file("running-example.xes")
        csv_export_traces_file.export_to_path(log, "ru.csv", ",", "case:concept:name", "concept:name")
        os.remove("ru.csv")

if __name__ == "__main__":
    unittest.main()
