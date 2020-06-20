from micropm4py.log import xes_import_traces_file_minimal_dfg
from micropm4py.discovery import alpha

log_path = "running-example.xes"

dfg = xes_import_traces_file_minimal_dfg.imp_dfg_file(log_path)
net, im, fm = alpha.alpha(dfg)
print(net)
