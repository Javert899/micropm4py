import gc
from micropm4py.petrinet import petrinet_import_file

model_path = "running-example.pnml"
net, im, fm = petrinet_import_file.imp_file(model_path)
del model_path
gc.collect()

from micropm4py.log import xes_import_traces_file_minimal_it
from micropm4py.petrinet import alignments

log_path = "running-example.xes"

# creates an iterator from the log: a single trace is fetched per time
it = xes_import_traces_file_minimal_it.get_it_from_file(log_path)
# let's pick the first trace
nxt = xes_import_traces_file_minimal_it.get_nxt_trace(it)
while nxt:
    # performs the alignments operation and print the alignment
    print(alignments.apply(nxt, net, im, fm))
    # let's pick the next trace
    nxt = xes_import_traces_file_minimal_it.get_nxt_trace(it)
