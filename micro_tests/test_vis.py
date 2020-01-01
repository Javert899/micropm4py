import unittest
from micropm4py.log import xes_import_traces_file_standard
from micropm4py.petrinet import petrinet_import_file
from micropm4py.visualization import dfg_print, petri_print


class TestVis(unittest.TestCase):
    def test_dfg_vis(self):
        dfg = xes_import_traces_file_standard.imp_dfg_file("running-example.xes")
        dfg_print.prnt_dot(dfg)

    def test_petri_vis(self):
        net, im, fm = petrinet_import_file.imp_file("running-example.pnml")
        petri_print.print_dot(net)


if __name__ == "__main__":
    unittest.main()
