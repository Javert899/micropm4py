try:
    import heapq
except:
    import uheaqp as heapq

try:
    import time
except:
    import utime as time

PLACES_DICT = "places_dict"
INV_TRANS_DICT = "inv_trans_dict"
LABELS_DICT = "labels_dict"
TRANS_LABELS_DICT = "trans_labels_dict"
TRANS_PRE_DICT = "trans_pre_dict"
TRANS_POST_DICT = "trans_post_dict"
TRANSF_IM = "transf_im"
TRANSF_FM = "transf_fm"
TRANSF_MODEL_COST_FUNCTION = "transf_model_cost_function"
TRANSF_TRACE = "transf_trace"
TRACE_COST_FUNCTION = "trace_cost_function"
INV_TRACE_LABELS_DICT = "inv_trace_labels_dict"

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
    model_struct = __transform_model_to_mem_efficient_structure(net, im, fm, model_cost_function=model_cost_function)
    trace_struct = __transform_trace_to_mem_efficient_structure(trace, model_struct, trace_cost_function=trace_cost_function)

    return __dijkstra(model_struct, trace_struct, net, ret_tuple_as_trans_desc=ret_tuple_as_trans_desc)


def __transform_model_to_mem_efficient_structure(net, im, fm, model_cost_function=None):
    """
    Transform the Petri net model to a memory efficient structure

    Parameters
    --------------
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    model_cost_function
        Model cost function

    Returns
    --------------
    model_struct
        Model data structure, including:
            PLACES_DICT: associates each place to a number
            INV_TRANS_DICT: associates a number to each transition
            LABELS_DICT: labels dictionary (a label to a number)
            TRANS_LABELS_DICT: associates each transition to the number corresponding to its label
            TRANS_PRE_DICT: preset of a transition, expressed as in this data structure
            TRANS_POST_DICT: postset of a transition, expressed as in this data structure
            TRANSF_IM: transformed initial marking
            TRANSF_FM: transformed final marking
            TRANSF_MODEL_COST_FUNCTION: transformed model cost function
    """
    if model_cost_function is None:
        model_cost_function = {}
        i = 0
        while i < len(net[1]):
            model_cost_function[i] = 10000
            i = i + 1

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
    trans_labels_dict = {}
    i = 0
    while i < len(net[1]):
        trans_labels_dict[i] = labels_dict[net[1][i][0]]
        i = i + 1

    return {TRANSF_MODEL_COST_FUNCTION: model_cost_function, TRANS_PRE_DICT: trans_pre_dict,
            TRANS_POST_DICT: trans_post_dict, TRANSF_IM: im,
            TRANSF_FM: fm, LABELS_DICT: labels_dict, TRANS_LABELS_DICT: trans_labels_dict}


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
    return {TRANSF_TRACE: transf_trace, TRACE_COST_FUNCTION: trace_cost_function,
            INV_TRACE_LABELS_DICT: inv_trace_labels_dict}


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


def __dijkstra(model_struct, trace_struct, net, sync_cost=0, max_align_time_trace=10000000,
               ret_tuple_as_trans_desc=False):
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
    sync_cost
        Cost of a sync move (limitation: all sync moves shall have the same cost in this setting)
    max_align_time_trace
        Maximum alignment time for a trace (in seconds)
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
    start_time = time.time()

    trans_pre_dict = model_struct[TRANS_PRE_DICT]
    trans_post_dict = model_struct[TRANS_POST_DICT]
    trans_labels_dict = model_struct[TRANS_LABELS_DICT]
    transf_model_cost_function = model_struct[TRANSF_MODEL_COST_FUNCTION]

    transf_trace = trace_struct[TRANSF_TRACE]
    trace_cost_function = trace_struct[TRACE_COST_FUNCTION]

    im = model_struct[TRANSF_IM]
    fm = model_struct[TRANSF_FM]

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
        if (time.time() - start_time) > max_align_time_trace:
            return None
        curr = heapq.heappop(open_set)
        visited = visited + 1
        if curr[POSITION_MARKING] == fm:
            if -curr[POSITION_INDEX] == len(transf_trace):
                # returns the alignment only if the final marking has been reached AND
                # the trace is over
                return __reconstruct_alignment(curr, model_struct, trace_struct, visited, net,
                                               ret_tuple_as_trans_desc=ret_tuple_as_trans_desc)
        else:
            # retrieves the transitions that are enabled in the current marking
            en_t = [t for t in trans_pre_dict if __dict_leq(trans_pre_dict[t], curr[POSITION_MARKING])]
            for t in en_t:
                # checks if a given transition can be executed in sync with the trace
                is_sync = trans_labels_dict[t] == transf_trace[-curr[POSITION_INDEX]] if -curr[POSITION_INDEX] < len(
                    transf_trace) else False
                # virtually fires the transition to get a new marking
                new_m = __fire_trans(curr[POSITION_MARKING], trans_pre_dict[t], trans_post_dict[t])
                if is_sync:
                    dummy_count = dummy_count + 1
                    new_state = (
                        curr[POSITION_TOTAL_COST] + sync_cost, curr[POSITION_INDEX] - 1, IS_SYNC_MOVE, dummy_count,
                        curr,
                        new_m, t)
                    heapq.heappush(open_set, new_state)
                dummy_count = dummy_count + 1
                new_state = (
                    curr[POSITION_TOTAL_COST] + transf_model_cost_function[t], curr[POSITION_INDEX], IS_MODEL_MOVE,
                    dummy_count, curr, new_m, t)
                heapq.heappush(open_set, new_state)
        # IMPORTANT: to reduce the complexity, assume that you can schedule a log move
        # only if the previous move has not been a move-on-model.
        # since this setting is equivalent to scheduling all the log moves before and then
        # the model moves
        if -curr[POSITION_INDEX] < len(transf_trace) and curr[POSITION_TYPE_MOVE] != IS_MODEL_MOVE:
            dummy_count = dummy_count + 1
            new_state = (
                curr[POSITION_TOTAL_COST] + trace_cost_function[-curr[POSITION_INDEX]], curr[POSITION_INDEX] - 1,
                IS_LOG_MOVE, dummy_count, curr, curr[POSITION_MARKING], None)
            heapq.heappush(open_set, new_state)


def __reconstruct_alignment(curr, model_struct, trace_struct, visited, net, ret_tuple_as_trans_desc=False):
    """
    Reconstruct the alignment from the final state (that reached the final marking)

    Parameters
    ----------------
    curr
        Current state (final state)
    model_struct
        Efficient data structure for the model
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
