from micropm4py.log import xes_import_traces_file
from micropm4py.discovery import alpha
from micropm4py.visualization import petri_print


log_path = "running-example.xes"

dfg = xes_import_traces_file.imp_dfg_file(log_path)
net, im, fm = alpha.alpha(dfg)
petri_print.print_dot(net)
