from micropm4py.petrinet import petrinet_exec, petrinet_import, petrinet_export, petrinet_import_file, petrinet_export_file
import unittest
import os


class TestPetri(unittest.TestCase):
    def test_petri_exec(self):
        petrinet_exec.main()

    def test_petri_import(self):
        petrinet_import.main()

    def test_petri_export(self):
        petrinet_export.main()

    def test_petri_import_export_file(self):
        net, im, fm = petrinet_import_file.imp_file("running-example.pnml")
        petrinet_export_file.export(net, im, fm, "ru.pnml")
        net, im, fm = petrinet_import_file.imp_file("ru.pnml")
        petrinet_export_file.export(net, im, fm, "ru2.pnml")
        os.remove("ru.pnml")
        os.remove("ru2.pnml")

if __name__ == "__main__":
    unittest.main()
