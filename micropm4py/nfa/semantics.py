def accept(nfa, state, stringu):
    state = tuple(state)
    i = 0
    while i < len(stringu):
        state = execute(nfa, state, stringu[i])
        i = i + 1
    if 1 in state:
        return True
    else:
        return False


def execute(nfa, state, label):
    estate = list(expand_state(nfa, state))
    new_state = set()
    i = 0
    while i < len(estate):
        j = 0
        while j < len(nfa[estate[i]]):
            if nfa[estate[i]][j][1] == label or nfa[estate[i]][j][1] == ".":
                new_state.add(nfa[estate[i]][j][0])
            j = j + 1
        i = i + 1
    return tuple(new_state)


def enabled_transitions(nfa, state):
    trans = set()
    estate = expand_state(nfa, state)
    i = 0
    while i < len(estate):
        j = 0
        while j < len(nfa[estate[i]]):
            if nfa[estate[i]][j][1] is not None:
                trans.add(nfa[estate[i]][j][1])
            j = j + 1
        i = i + 1
    return tuple(trans)


def expand_state(nfa, state):
    state = set(state)
    to_visit = list(state)
    while to_visit:
        ss = to_visit.pop(0)
        iv = reachable_invisible(nfa, ss)
        i = 0
        while i < len(iv):
            if not iv[i] in state:
                state.add(iv[i])
                to_visit.append(iv[i])
            i = i + 1
    return tuple(state)


def reachable_invisible(nfa, node):
    reach = set()
    reach.add(node)
    to_visit = list(reach)
    while to_visit:
        ss = to_visit.pop(0)
        i = 0
        while i < len(nfa[ss]):
            if nfa[ss][i][1] is None:
                if not nfa[ss][i][0] in reach:
                    reach.add(nfa[ss][i][0])
                    to_visit.append(nfa[ss][i][0])
            i = i + 1
    return tuple(reach)
