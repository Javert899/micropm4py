from micropm4py.log import xes_import_traces_file_minimal_it
from micropm4py.petrinet import alignments

log_path = "running-example.xes"

net = ((0, 0, 0, 0, 0, 0, 0), (('decide', (5, 2), (4,)), ('examine casually', (6,), (2,)), ('examine thoroughly', (6,), (2,)), ('register request', (0,), (1, 6)), ('check ticket', (1,), (5,)), ('reinitiate request', (4,), (6, 1)), ('pay compensation', (4,), (3,)), ('reject request', (4,), (3,))))
im = {0: 1}
fm = {3: 1}

# creates an iterator from the log: a single trace is fetched per time
it = xes_import_traces_file_minimal_it.get_it_from_file(log_path)
# let's pick the first trace
nxt = xes_import_traces_file_minimal_it.get_nxt_trace(it)
while nxt:
    # performs the alignments operation and print the alignment
    print(alignments.apply(nxt, net, im, fm))
    # let's pick the next trace
    nxt = xes_import_traces_file_minimal_it.get_nxt_trace(it)
