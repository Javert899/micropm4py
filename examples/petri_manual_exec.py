from micropm4py.petrinet import petrinet_import_file
from micropm4py.util import copy
from micropm4py.petrinet import petrinet_exec


def main():
    net, im, fm = petrinet_import_file.imp_file("../micro_tests/running-example.pnml")
    # TRIAL 1 - Manually execute the Petri net
    m = copy.copy(im)
    print(m)
    petrinet_exec.exec(net, m, "register request")
    # at this point, two tokens are in the net (since check ticket and examine casually/examine throughly
    # are concurrent)
    print(m)
    petrinet_exec.exec(net, m, "examine casually")
    petrinet_exec.exec(net, m, "check ticket")
    petrinet_exec.exec(net, m, "decide")
    petrinet_exec.exec(net, m, "pay compensation")
    print(m, fm, m == fm)
    # TRIAL 2 - Execute some traces on the Petri net and see if they fit
    m = copy.copy(im)
    # correct execution: the result is True
    res = petrinet_exec.ex_trace(net, m, fm, ["register request", "examine casually", "check ticket", "decide", "pay compensation"])
    print(res)
    # incorrect execution (check ticket is missing): the result is False
    res = petrinet_exec.ex_trace(net, m, fm, ["register request", "examine casually", "decide", "pay compensation"])
    print(res)
    # incorrect execution (the trace til decide is correct, but one between pay compensation and reject request is missing,
    # so the final marking is not reached)
    res = petrinet_exec.ex_trace(net, m, fm, ["register request", "examine casually", "check ticket", "decide"])
    print(res)


if __name__ == "__main__":
    main()
