import gc
from micropm4py.log import xes_import_traces_file_minimal_dfg

log_path = "running-example.xes"

dfg = xes_import_traces_file_minimal_dfg.imp_dfg_file(log_path)
dfg = tuple(dfg)
print(dfg)
del log_path
gc.collect()

from micropm4py.discovery import alpha

net, im, fm = alpha.alpha(dfg)
print(net)

del dfg
gc.collect()

from micropm4py.visualization import petri_print
petri_print.print_dot(net)
