from micropm4py.log import dfg_import_export
from micropm4py.discovery import alpha
from micropm4py.visualization import petri_print
import time
import os


def main():
    dfg = dfg_import_export.import_dfg(os.path.join("..", "micro_tests", "running-example.dfg"))
    net, im, fm = alpha.alpha(dfg)
    dfg_import_export.print_dfg(dfg)


if __name__ == "__main__":
    time.ticks_ms = time.time
    main()
