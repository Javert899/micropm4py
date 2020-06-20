net = ((0, 0, 0, 0, 0, 0, 0), (('decide', (5, 2), (4,)), ('examine casually', (6,), (2,)), ('examine thoroughly', (6,), (2,)), ('register request', (0,), (1, 6)), ('check ticket', (1,), (5,)), ('reinitiate request', (4,), (6, 1)), ('pay compensation', (4,), (3,)), ('reject request', (4,), (3,))))
im = {0: 1}
fm = {3: 1}

from micropm4py.log import xes_import_traces_file_minimal
from micropm4py.petrinet import petrinet_exec
from micropm4py.util import copy

log_path = "running-example.xes"

# reads the Petri net model
# creates an iterator from the log: a single trace is fetched per time
it = xes_import_traces_file_minimal.get_it_from_file(log_path)
# let's pick the first trace
nxt = xes_import_traces_file_minimal.get_nxt_trace(it)
while nxt:
    # performs the token-based replay operation (that returns True if the trace fits,
    # False if the trace does not fit)
    print(petrinet_exec.ex_trace(net, copy.copy(im), copy.copy(fm), nxt[1]))
    # let's pick the next trace
    nxt = xes_import_traces_file_minimal.get_nxt_trace(it)
