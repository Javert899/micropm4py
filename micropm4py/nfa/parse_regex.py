def parse(regex):
    tokens = [(regex.index("^")+1, regex.index("$")-1, 0, 1)]
    nfa = [[], []]
    i = 0
    j = 0
    z = 0
    par_lev = 0
    conjtype = 0
    while tokens:
        token = tokens.pop(0)
        if token[1] - token[0] == 0:
            nfa[token[2]].append((token[3], regex[token[0]]))
        else:
            subtokens = []
            opmem = {}
            conjtype = 0
            i = token[0]
            while i <= token[1]:
                if regex[i] == "|":
                    conjtype = 1
                elif regex[i] in ("*", "+", "?"):
                    opmem[len(subtokens)-1] = regex[i]
                elif regex[i] == "(":
                    par_lev = 1
                    z = i + 1
                    while z <= token[1]:
                        if regex[z] == "(":
                            par_lev = par_lev + 1
                        elif regex[z] == ")":
                            par_lev = par_lev - 1
                            if par_lev == 0:
                                left = i + 1
                                right = z - 1
                                if conjtype == 0:
                                    if not subtokens:
                                        subtokens.append([left, right, token[2], None])
                                    else:
                                        nfa.append([])
                                        j = len(subtokens) - 1
                                        while j >= 0:
                                            if subtokens[j][3] is None:
                                                subtokens[j][3] = len(nfa) - 1
                                            if j in opmem:
                                                if opmem[j] in ("*", "+"):
                                                    if not [subtokens[j][2], None] in nfa[subtokens[j][3]]:
                                                        nfa[subtokens[j][3]].append([subtokens[j][2], None])
                                                if opmem[j] in ("*", "?"):
                                                    if not [subtokens[j][3], None] in nfa[subtokens[j][2]]:
                                                        nfa[subtokens[j][2]].append([subtokens[j][3], None])
                                                del opmem[j]
                                            subtokens[j] = tuple(subtokens[j])
                                            j = j - 1
                                        subtokens.append([left, right, subtokens[-1][3], None])
                                elif conjtype == 1:
                                    subtokens.append([left, right, subtokens[-1][2], None])
                                conjtype = 0
                                break

                        z = z + 1
                    i = z
                else:
                    if conjtype == 0:
                        if not subtokens:
                            subtokens.append([i, i, token[2], None])
                        else:
                            nfa.append([])
                            j = len(subtokens)-1
                            while j >= 0:
                                if subtokens[j][3] is None:
                                    subtokens[j][3] = len(nfa)-1
                                if j in opmem:
                                    if opmem[j] in ("*", "+"):
                                        if not [subtokens[j][2], None] in nfa[subtokens[j][3]]:
                                            nfa[subtokens[j][3]].append([subtokens[j][2], None])
                                    if opmem[j] in ("*", "?"):
                                        if not [subtokens[j][3], None] in nfa[subtokens[j][2]]:
                                            nfa[subtokens[j][2]].append([subtokens[j][3], None])
                                    del opmem[j]
                                subtokens[j] = tuple(subtokens[j])
                                j = j - 1
                            subtokens.append([i, i, subtokens[-1][3], None])
                    elif conjtype == 1:
                        subtokens.append([i, i, subtokens[-1][2], None])
                    conjtype = 0
                i = i + 1
            j = len(subtokens)-1
            while j >= 0:
                if subtokens[j][3] is None:
                    subtokens[j][3] = token[3]
                subtokens[j] = tuple(subtokens[j])
                j = j - 1
            for j in opmem:
                if opmem[j] in ("*", "+"):
                    if not [subtokens[j][2], None] in nfa[subtokens[j][3]]:
                        nfa[subtokens[j][3]].append([subtokens[j][2], None])
                if opmem[j] in ("*", "?"):
                    if not [subtokens[j][3], None] in nfa[subtokens[j][2]]:
                        nfa[subtokens[j][2]].append([subtokens[j][3], None])
            while subtokens:
                subt = subtokens.pop(0)
                tokens.append(subt)
    i = 0
    while i < len(nfa):
        nfa[i] = tuple(nfa[i])
        i = i + 1
    nfa = tuple(nfa)
    return nfa

