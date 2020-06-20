try:
    import heapq
except:
    import uheaqp as heapq

import gc

TRANSF_MODEL_COST_FUNCTION = 0
TRANS_PRE_DICT = 1
TRANS_POST_DICT = 2
LABELS_DICT = 3
TRANS_LABELS_DICT = 4

TRANSF_TRACE = 0
TRACE_COST_FUNCTION = 1
INV_TRACE_LABELS_DICT = 2

IS_SYNC_MOVE = 0
IS_LOG_MOVE = 1
IS_MODEL_MOVE = 2

POSITION_TOTAL_COST = 0
POSITION_INDEX = 1
POSITION_TYPE_MOVE = 2
POSITION_STATES_COUNT = 3
POSITION_PARENT_STATE = 4
POSITION_MARKING = 5
POSITION_EN_T = 6


def apply(trace, net, im, fm, model_cost_function=None, trace_cost_function=None, ret_tuple_as_trans_desc=False,
          enable_gc=True):
    model_struct = __transform_model_to_mem_efficient_structure(net, model_cost_function=model_cost_function)
    trace_struct = __transform_trace_to_mem_efficient_structure(trace, model_struct,
                                                                trace_cost_function=trace_cost_function)

    return __dijkstra(model_struct, trace_struct, net, im, fm, ret_tuple_as_trans_desc=ret_tuple_as_trans_desc,
                      enable_gc=enable_gc)


def __transform_model_to_mem_efficient_structure(net, model_cost_function=None):
    if model_cost_function is None:
        model_cost_function = []
        i = 0
        while i < len(net[1]):
            model_cost_function.append(10000)
            i = i + 1
        model_cost_function = tuple(model_cost_function)

    trans_pre_dict = {}
    trans_post_dict = {}
    labels = set()
    i = 0
    while i < len(net[1]):
        trans_pre_dict[i] = {x: 1 for x in net[1][i][1]}
        trans_post_dict[i] = {x: 1 for x in net[1][i][2]}
        labels.add(net[1][i][0])
        i = i + 1
    labels = sorted(list(labels))
    labels_dict = {labels[i]: i for i in range(len(labels))}
    trans_labels_dict = []
    i = 0
    while i < len(net[1]):
        trans_labels_dict.append(labels_dict[net[1][i][0]])
        i = i + 1
    trans_labels_dict = tuple(trans_labels_dict)

    return (model_cost_function, trans_pre_dict, trans_post_dict, labels_dict, trans_labels_dict)


def __transform_trace_to_mem_efficient_structure(trace, model_struct, trace_cost_function=None):
    if trace_cost_function is None:
        trace_cost_function = {i: 10000 for i in range(len(trace[1]))}

    labels = sorted(list(set(x for x in trace[1])))
    labels_dict = {}
    for x in model_struct[LABELS_DICT]:
        labels_dict[x] = model_struct[LABELS_DICT][x]

    for l in labels:
        if l not in labels_dict:
            labels_dict[l] = len(labels_dict)

    transf_trace = [labels_dict[x] for x in trace[1]]

    inv_trace_labels_dict = {y: x for x, y in labels_dict.items()}

    return (transf_trace, trace_cost_function, inv_trace_labels_dict)


def __dict_leq(d1, d2):
    for k in d1:
        if k not in d2:
            return False
        if d1[k] > d2[k]:
            return False
    return True


def __fire_trans(m, preset, postset):
    ret = {}
    for k in m:
        if k in preset:
            diff = m[k] - preset[k]
            if diff > 0:
                ret[k] = diff
        else:
            ret[k] = m[k]
    for k in postset:
        if k not in ret:
            ret[k] = postset[k]
        else:
            ret[k] = ret[k] + postset[k]
    return ret


def __encode_marking(existing_markings, m_d):
    keys = sorted(list(m_d.keys()))
    m_t = []
    for el in keys:
        for i in range(m_d[el]):
            m_t.append(el)
    m_t = tuple(m_t)
    i = 0
    while i < len(existing_markings):
        if existing_markings[i] == m_t:
            return existing_markings, existing_markings[i]
        i = i + 1
    existing_markings = existing_markings + (m_t,)
    return existing_markings, m_t


def __decode_marking(m_t):
    m_d = {}
    for el in m_t:
        if el not in m_d:
            m_d[el] = 1
        else:
            m_d[el] = m_d[el] + 1

    return m_d


def __check_closed(closed, ns):
    if ns[0] in closed and closed[ns[0]] <= ns[1]:
        return True
    return False


def __add_closed(closed, ns):
    closed[ns[0]] = ns[1]


def __add_to_open_set(open_set, ns):
    shall_add = True
    shall_heapify = False
    i = 0
    while i < len(open_set):
        if open_set[i][POSITION_MARKING] == ns[POSITION_MARKING]:
            if open_set[i][POSITION_INDEX] <= ns[POSITION_INDEX] and open_set[i][POSITION_TOTAL_COST] <= ns[
                POSITION_TOTAL_COST]:
                # do not add anything
                shall_add = False
                break
            if open_set[i][POSITION_INDEX] >= ns[POSITION_INDEX] and open_set[i][POSITION_TOTAL_COST] > ns[
                POSITION_TOTAL_COST]:
                del open_set[i]
                shall_heapify = True
                continue
        i = i + 1
    if shall_add:
        heapq.heappush(open_set, ns)
    if shall_heapify:
        heapq.heapify(open_set)
    return open_set


def __dijkstra(model_struct, trace_struct, net, im, fm, sync_cost=0, ret_tuple_as_trans_desc=False, enable_gc=True):
    trans_pre_dict = model_struct[TRANS_PRE_DICT]
    trans_post_dict = model_struct[TRANS_POST_DICT]
    trans_labels_dict = model_struct[TRANS_LABELS_DICT]
    transf_model_cost_function = model_struct[TRANSF_MODEL_COST_FUNCTION]

    transf_trace = trace_struct[TRANSF_TRACE]
    trace_cost_function = trace_struct[TRACE_COST_FUNCTION]

    existing_markings = tuple([])
    closed = {}

    existing_markings, im = __encode_marking(existing_markings, im)
    existing_markings, fm = __encode_marking(existing_markings, fm)

    initial_state = (0, 0, 0, 0, None, im, None)
    open_set = [initial_state]
    heapq.heapify(open_set)

    dummy_count = 0
    visited = 0

    while not len(open_set) == 0:
        curr = heapq.heappop(open_set)
        visited = visited + 1
        if __check_closed(closed, (curr[POSITION_MARKING], curr[POSITION_INDEX])):
            continue
        if curr[POSITION_MARKING] == fm:
            if -curr[POSITION_INDEX] == len(transf_trace):
                # returns the alignment only if the final marking has been reached AND
                # the trace is over
                return __reconstruct_alignment(curr, trace_struct, net, visited, len(open_set), len(closed),
                                               len(existing_markings),
                                               ret_tuple_as_trans_desc=ret_tuple_as_trans_desc)
            else:
                __add_closed(closed, (curr[POSITION_MARKING], curr[POSITION_INDEX]))
        else:
            __add_closed(closed, (curr[POSITION_MARKING], curr[POSITION_INDEX]))
            curr_m = __decode_marking(curr[POSITION_MARKING])
            # retrieves the transitions that are enabled in the current marking
            en_t = tuple([t for t in trans_pre_dict if __dict_leq(trans_pre_dict[t], curr_m)])
            for t in en_t:
                # checks if a given transition can be executed in sync with the trace
                is_sync = trans_labels_dict[t] == transf_trace[-curr[POSITION_INDEX]] if -curr[POSITION_INDEX] < len(
                    transf_trace) else False
                # virtually fires the transition to get a new marking
                existing_markings, new_m = __encode_marking(existing_markings,
                                                            __fire_trans(curr_m, trans_pre_dict[t], trans_post_dict[t]))
                if is_sync:
                    dummy_count = dummy_count + 1
                    if not __check_closed(closed, (new_m, curr[POSITION_INDEX] - 1)):
                        new_state = (
                            curr[POSITION_TOTAL_COST] + sync_cost, curr[POSITION_INDEX] - 1, IS_SYNC_MOVE, dummy_count,
                            curr,
                            new_m, t)
                        open_set = __add_to_open_set(open_set, new_state)
                else:
                    # avoid scheduling a move-on-model when model and trace are sync.
                    dummy_count = dummy_count + 1
                    if not __check_closed(closed, (new_m, curr[POSITION_INDEX] - 1)):
                        new_state = (
                            curr[POSITION_TOTAL_COST] + transf_model_cost_function[t], curr[POSITION_INDEX],
                            IS_MODEL_MOVE,
                            dummy_count, curr, new_m, t)
                        open_set = __add_to_open_set(open_set, new_state)
        # IMPORTANT: to reduce the complexity, assume that you can schedule a log move
        # only if the previous move has not been a move-on-model.
        # since this setting is equivalent to scheduling all the log moves before and then
        # the model moves
        if -curr[POSITION_INDEX] < len(transf_trace) and curr[POSITION_TYPE_MOVE] != IS_MODEL_MOVE:
            dummy_count = dummy_count + 1
            if not __check_closed(closed, (curr[POSITION_MARKING], curr[POSITION_INDEX] - 1)):
                new_state = (
                    curr[POSITION_TOTAL_COST] + trace_cost_function[-curr[POSITION_INDEX]], curr[POSITION_INDEX] - 1,
                    IS_LOG_MOVE, dummy_count, curr, curr[POSITION_MARKING], None)
                open_set = __add_to_open_set(open_set, new_state)
        if enable_gc:
            gc.collect()


def __reconstruct_alignment(curr, trace_struct, net, visited, queued, closed_set_length, num_visited_markings,
                            ret_tuple_as_trans_desc=False):
    transf_trace = trace_struct[TRANSF_TRACE]
    inv_labels_dict = trace_struct[INV_TRACE_LABELS_DICT]

    alignment = []
    cost = curr[POSITION_TOTAL_COST]

    queued = queued + visited

    while curr[POSITION_PARENT_STATE] is not None:
        m_name, m_label, t_name, t_label = ">>", ">>", ">>", ">>"
        if curr[POSITION_TYPE_MOVE] == IS_SYNC_MOVE or curr[POSITION_TYPE_MOVE] == IS_LOG_MOVE:
            name = inv_labels_dict[transf_trace[-curr[POSITION_INDEX] - 1]]
            t_name, t_label = name, name
        if curr[POSITION_TYPE_MOVE] == IS_SYNC_MOVE or curr[POSITION_TYPE_MOVE] == IS_MODEL_MOVE:
            t = net[1][curr[POSITION_EN_T]][0]
            m_name, m_label = t, t

        if ret_tuple_as_trans_desc:
            alignment = [((t_name, m_name), (t_label, m_label))] + alignment
        else:
            alignment = [(t_label, m_label)] + alignment
        curr = curr[POSITION_PARENT_STATE]

    return {"alignment": alignment, "cost": cost, "queued_states": queued, "visited_states": visited,
            "closed_set_length": closed_set_length, "num_visited_markings": num_visited_markings}
