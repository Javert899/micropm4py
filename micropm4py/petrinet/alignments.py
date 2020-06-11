try:
    import heapq
except:
    import uheaqp as heapq


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


def apply(trace, net, im, fm, model_cost_function=None, trace_cost_function=None, ret_tuple_as_trans_desc=False):
    """
    Apply alignments using the Dijkstra approach

    Parameters
    ---------------
    trace
        Trace
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    model_cost_function
        Model cost function
    trace_cost_function
        Trace cost function
    ret_tuple_as_trans_desc
        Return tuple as trans desc
    """
    model_struct = __transform_model_to_mem_efficient_structure(net, model_cost_function=model_cost_function)
    trace_struct = __transform_trace_to_mem_efficient_structure(trace, model_struct, trace_cost_function=trace_cost_function)

    return __dijkstra(model_struct, trace_struct, net, im, fm, ret_tuple_as_trans_desc=ret_tuple_as_trans_desc)


def __transform_model_to_mem_efficient_structure(net, model_cost_function=None):
    """
    Transform the Petri net model to a memory efficient structure

    Parameters
    --------------
    net
        Petri net
    model_cost_function
        Model cost function

    Returns
    --------------
    model_struct
        Model data structure, including:
            TRANSF_MODEL_COST_FUNCTION: transformed model cost function
            TRANS_PRE_DICT: preset of a transition, expressed as in this data structure
            TRANS_POST_DICT: postset of a transition, expressed as in this data structure
            LABELS_DICT: labels dictionary (a label to a number)
            TRANS_LABELS_DICT: associates each transition to the number corresponding to its label
    """
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
    """
    Transforms a trace to a memory efficient structure

    Parameters
    ---------------
    trace
        Trace
    model_struct
        Efficient data structure for the model (calculated above)

    Returns
    ---------------
    trace_struct
        An efficient structure describing the trace, including:
            TRANSF_TRACE: the transformed trace
            TRACE_COST_FUNCTION: the cost function associated to the trace
            INV_TRACE_LABELS_DICT: dictionary that associates a number to an activity
    """
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
    """
    Checks if the first dictionary is <= the second

    Parameters
    --------------
    d1
        First dictionary
    d2
        Second dictionary

    Returns
    --------------
    boolean
        Boolean
    """
    for k in d1:
        if k not in d2:
            return False
        if d1[k] > d2[k]:
            return False
    return True


def __fire_trans(m, preset, postset):
    """
    Fires a transition and returns a new marking

    Parameters
    ---------------
    m
        Marking
    preset
        Preset
    postset
        Postset

    Returns
    ---------------
    new_m
        New marking
    """
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


def __encode_marking(marking_dict, m_d):
    """
    Encode a marking using the dictionary

    Parameters
    --------------
    marking_dict
        Marking dictionary
    m_d
        Current marking (dict)

    Returns
    --------------
    m_t
        Marking in tuple
    """
    keys = sorted(list(m_d.keys()))
    m_t = []
    for el in keys:
        for i in range(m_d[el]):
            m_t.append(el)
    m_t = tuple(m_t)
    if m_t not in marking_dict:
        marking_dict[m_t] = m_t
    return marking_dict[m_t]


def __decode_marking(m_t):
    """
    Decode a marking using a dictionary

    Parameters
    ---------------
    m_t
        Marking as tuple

    Returns
    ---------------
    m_d
        Marking as dictionary
    """
    m_d = {}
    for el in m_t:
        if el not in m_d:
            m_d[el] = 1
        else:
            m_d[el] = m_d[el] + 1

    return m_d


def __add_to_open_set(open_set, ns):
    """
    Adds a new state to the open set whether necessary

    Parameters
    ----------------
    open_set
        Open set
    ns
        New state
    """
    shall_add = True
    shall_heapify = False
    i = 0
    while i < len(open_set):
        if open_set[i][POSITION_MARKING] == ns[POSITION_MARKING]:
            if open_set[i][POSITION_INDEX] <= ns[POSITION_INDEX] and open_set[i][POSITION_TOTAL_COST] <= ns[POSITION_TOTAL_COST]:
                # do not add anything
                shall_add = False
                break
            if open_set[i][POSITION_INDEX] >= ns[POSITION_INDEX] and open_set[i][POSITION_TOTAL_COST] > ns[POSITION_TOTAL_COST]:
                del open_set[i]
                shall_heapify = True
                continue
        i = i + 1
    if shall_add:
        heapq.heappush(open_set, ns)
    if shall_heapify:
        heapq.heapify(open_set)
    return open_set


def __dijkstra(model_struct, trace_struct, net, im, fm, sync_cost=0, ret_tuple_as_trans_desc=False):
    """
    Alignments using Dijkstra

    Parameters
    ---------------
    model_struct
        Efficient model structure
    trace_struct
        Efficient trace structure
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    sync_cost
        Cost of a sync move (limitation: all sync moves shall have the same cost in this setting)
    ret_tuple_as_trans_desc
        Says if the alignments shall be constructed including also
        the name of the transition, or only the label (default=False includes only the label)

    Returns
    --------------
    alignment
        Alignment of the trace, including:
            alignment: the sequence of moves
            queued: the number of states that have been queued
            visited: the number of states that have been visited
            cost: the cost of the alignment
    """
    trans_pre_dict = model_struct[TRANS_PRE_DICT]
    trans_post_dict = model_struct[TRANS_POST_DICT]
    trans_labels_dict = model_struct[TRANS_LABELS_DICT]
    transf_model_cost_function = model_struct[TRANSF_MODEL_COST_FUNCTION]

    transf_trace = trace_struct[TRANSF_TRACE]
    trace_cost_function = trace_struct[TRACE_COST_FUNCTION]

    marking_dict = {}
    closed = set()

    im = __encode_marking(marking_dict, im)
    fm = __encode_marking(marking_dict, fm)

    # each state is characterized by:
    # position 0 (POSITION_TOTAL_COST): total cost of the state
    # position 1 (POSITION_INDEX): the opposite of the position of the trace (the higher is, the lower should
    # be the state in the queue
    # position 2 (POSITION_TYPE_MOVE): the type of the move:
    # ----------- 0 (IS_SYNC_MOVE): sync moves
    # ----------- 1 (IS_LOG_MOVE): log moves
    # ----------- 2 (IS_MODEL_MOVE): model moves
    # position 3 (POSITION_STATES_COUNT): the count of states visited
    # position 4 (POSITION_PARENT_STATE): if valued, the parent state of the current state
    # position 5 (POSITION_MARKING): the marking associated to the state
    # position 6 (POSITION_EN_T): if valued, the transition that was enabled to reach the state
    initial_state = (0, 0, 0, 0, None, im, None)
    open_set = [initial_state]
    heapq.heapify(open_set)

    dummy_count = 0
    visited = 0

    while not len(open_set) == 0:
        curr = heapq.heappop(open_set)
        curr_m0 = curr[POSITION_MARKING]
        if (curr_m0, curr[POSITION_INDEX]) in closed:
            continue
        closed.add((curr_m0, curr[POSITION_INDEX]))
        curr_m = __decode_marking(curr_m0)
        visited = visited + 1
        if curr_m0 == fm:
            if -curr[POSITION_INDEX] == len(transf_trace):
                # returns the alignment only if the final marking has been reached AND
                # the trace is over
                return __reconstruct_alignment(curr, trace_struct, visited, net,
                                               ret_tuple_as_trans_desc=ret_tuple_as_trans_desc)
        else:
            # retrieves the transitions that are enabled in the current marking
            en_t = [t for t in trans_pre_dict if __dict_leq(trans_pre_dict[t], curr_m)]
            for t in en_t:
                # checks if a given transition can be executed in sync with the trace
                is_sync = trans_labels_dict[t] == transf_trace[-curr[POSITION_INDEX]] if -curr[POSITION_INDEX] < len(
                    transf_trace) else False
                # virtually fires the transition to get a new marking
                new_m = __encode_marking(marking_dict, __fire_trans(curr_m, trans_pre_dict[t], trans_post_dict[t]))
                if is_sync:
                    dummy_count = dummy_count + 1
                    if (new_m, curr[POSITION_INDEX]-1) not in closed:
                        new_state = (
                            curr[POSITION_TOTAL_COST] + sync_cost, curr[POSITION_INDEX] - 1, IS_SYNC_MOVE, dummy_count,
                            curr,
                            new_m, t)
                        open_set = __add_to_open_set(open_set, new_state)
                else:
                    # avoid scheduling a move-on-model when model and trace are sync.
                    dummy_count = dummy_count + 1
                    new_state = (
                        curr[POSITION_TOTAL_COST] + transf_model_cost_function[t], curr[POSITION_INDEX], IS_MODEL_MOVE,
                        dummy_count, curr, new_m, t)
                    open_set = __add_to_open_set(open_set, new_state)
        # IMPORTANT: to reduce the complexity, assume that you can schedule a log move
        # only if the previous move has not been a move-on-model.
        # since this setting is equivalent to scheduling all the log moves before and then
        # the model moves
        if -curr[POSITION_INDEX] < len(transf_trace) and curr[POSITION_TYPE_MOVE] != IS_MODEL_MOVE:
            dummy_count = dummy_count + 1
            if (curr_m0, curr[POSITION_INDEX] - 1) not in closed:
                new_state = (
                    curr[POSITION_TOTAL_COST] + trace_cost_function[-curr[POSITION_INDEX]], curr[POSITION_INDEX] - 1,
                    IS_LOG_MOVE, dummy_count, curr, curr_m0, None)
                open_set = __add_to_open_set(open_set, new_state)


def __reconstruct_alignment(curr, trace_struct, visited, net, ret_tuple_as_trans_desc=False):
    """
    Reconstruct the alignment from the final state (that reached the final marking)

    Parameters
    ----------------
    curr
        Current state (final state)
    trace_struct
        Efficient data structure for the trace
    visited
        Number of visited states
    net
        Petri net
    ret_tuple_as_trans_desc
        Says if the alignments shall be constructed including also
        the name of the transition, or only the label (default=False includes only the label)

    Returns
    --------------
    alignment
        Alignment of the trace, including:
            alignment: the sequence of moves
            queued: the number of states that have been queued
            visited: the number of states that have been visited
            cost: the cost of the alignment
    """
    transf_trace = trace_struct[TRANSF_TRACE]
    inv_labels_dict = trace_struct[INV_TRACE_LABELS_DICT]

    alignment = []
    cost = curr[POSITION_TOTAL_COST]
    queued = curr[POSITION_STATES_COUNT]

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

    return {"alignment": alignment, "cost": cost, "queued_states": queued, "visited_states": visited}
