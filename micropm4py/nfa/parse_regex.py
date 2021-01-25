def parse(regex):
    tokens = [(regex.index("^")+1, regex.index("$")-1, 0, 1)]
    edges = [[], []]
    while tokens:
        token = tokens.pop(0)
        if regex[token[1]] in ("*", "+", "?"):
            if regex[token[1]-1] == ")":
                tokens.append((token[0]+1, token[1]-2, token[2], token[3]))
            else:
                tokens.append((token[0], token[1]-1, token[2], token[3]))
            if regex[token[1]] in ("*", "+"):
                edges[token[3]].append((token[2], None))
            if regex[token[1]] in ("*", "?"):
                edges[token[2]].append((token[3], None))
        elif token[1] - token[0] == 0:
            edges[token[2]].append((token[3], regex[token[0]]))
        else:
            subtokens = []
            conjtype = [0]
            i = token[0]
            while i <= token[1]:
                if regex[i] == "|":
                    conjtype[-1] = 1
                elif regex[i] == "(":
                    par_lev = 1
                    z = i + 1
                    while z <= token[1]:
                        if regex[z] == "(":
                            par_lev = par_lev + 1
                        elif regex[z] == ")":
                            par_lev = par_lev - 1
                            if par_lev == 0:
                                if z < token[1] and regex[z+1] in ("*", "+", "?"):
                                    left = i
                                    right = z+1
                                else:
                                    left = i+1
                                    right = z-1
                                if conjtype[-1] == 0:
                                    if not subtokens:
                                        subtokens.append([left, right, token[2], None])
                                    else:
                                        edges.append([])
                                        j = len(subtokens) - 1
                                        while j >= 0:
                                            if subtokens[j][3] is None:
                                                subtokens[j][3] = len(edges) - 1
                                            subtokens[j] = tuple(subtokens[j])
                                            j = j - 1
                                        subtokens.append([left, right, subtokens[-1][3], None])
                                elif conjtype[-1] == 1:
                                    subtokens.append([left, right, subtokens[-1][2], None])
                                conjtype.append(0)
                        z = z + 1
                    i = z
                else:
                    if conjtype[-1] == 0:
                        if not subtokens:
                            subtokens.append([i, i, token[2], None])
                        else:
                            edges.append([])
                            j = len(subtokens)-1
                            while j >= 0:
                                if subtokens[j][3] is None:
                                    subtokens[j][3] = len(edges)-1
                                subtokens[j] = tuple(subtokens[j])
                                j = j - 1
                            subtokens.append([i, i, subtokens[-1][3], None])
                    elif conjtype[-1] == 1:
                        subtokens.append([i, i, subtokens[-1][2], None])
                    conjtype.append(0)
                i = i + 1
            j = len(subtokens)-1
            while j >= 0:
                if subtokens[j][3] is None:
                    subtokens[j][3] = token[3]
                subtokens[j] = tuple(subtokens[j])
                j = j - 1
            while subtokens:
                subt = subtokens.pop(0)
                tokens.append(subt)
    return edges


def view_gg(gg):
    import tempfile
    from graphviz import Digraph
    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    filename.close()
    viz = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': 'transparent'})
    viz.graph_attr['rankdir'] = "LR"
    for i in range(len(gg)):
        viz.node(str(i))
    for i in range(len(gg)):
        for j in range(len(gg[i])):
            viz.edge(str(i), str(gg[i][j][0]), label=str(gg[i][j][1]))
    viz.attr(overlap='false')
    viz.attr(fontsize='11')

    viz.format = "png"

    return viz.view(cleanup=True)

#gg = parse("^adefgb|c$")
gg = parse("^(abc)+$")
print(gg)
view_gg(gg)
