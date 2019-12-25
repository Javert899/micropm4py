import unittest
import os
from micropm4py.conversion.pm4py import dfg as pm4py_dfg
from micropm4py.conversion.dfg import traces_to_dfg
from micropm4py.log import xes_import_traces_file


class TestConv(unittest.TestCase):
    def test_conv0(self):
        traces_to_dfg.main()

    def test_conv_log(self):
        traces = xes_import_traces_file.imp_list_traces_from_file("running-example.xes")
        dfg0 = traces_to_dfg.trs_to_dfg(traces)
        acti_count, dfg = pm4py_dfg.to(dfg0)
        print(acti_count)
        print(dfg)


if __name__ == "__main__":
    unittest.main()
