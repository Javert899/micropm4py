from micropm4py.log import xes_import_traces_file
from micropm4py.discovery import alpha
from micropm4py.visualization import petri_print

def main():
    dfg = xes_import_traces_file.imp_dfg_file("../micro_tests/running-example.xes")
    net, im, fm = alpha.alpha(dfg)
    petri_print.print_dot(net)


if __name__ == "__main__":
    main()
