def parse(regex):
    regex = regex[1:-1]
    level = 0
    left_connection = [0]
    right_connection = [1]
    start_level = [0]
    edges = [[], []]
    nodes_levels = [0, 0]
    i = 0
    while i < len(regex):
        if regex[i] == "(":
            level = level + 1
            edges.append([])
            edges.append([])
            nodes_levels.append(level)
            nodes_levels.append(level)
            if len(start_level) < level + 1:
                start_level.append(len(edges)-2)
            else:
                start_level[level] = len(edges)-2
            left_connection.append(len(edges)-2)
            right_connection.append(len(edges)-1)
            edges[left_connection[level-1]].append((left_connection[level], None))
        elif regex[i] == ")":
            level = level - 1
            left_connection[level] = right_connection[level]
            edges.append([])
            nodes_levels.append(level)
            right_connection[level] = len(edges) - 1
            if i < len(regex)-1 and regex[i+1] == "?":
                edges[start_level[level+1]].append((right_connection[level+1], None))
                i = i + 1
            elif i < len(regex)-1 and regex[i+1] == "*":
                edges[start_level[level+1]].append((right_connection[level+1], None))
                edges[right_connection[level+1]].append((start_level[level+1], None))
                i = i + 1
            elif i < len(regex)-1 and regex[i+1] == "+":
                edges[right_connection[level+1]].append((start_level[level+1], None))
                i = i + 1
            j = 0
            found = False
            while j < len(edges[left_connection[level+1]]):
                if edges[left_connection[level+1]][j][0] == right_connection[level+1]:
                    found = True
                    break
                j = j + 1
            if not found:
                edges[left_connection[level+1]].append((right_connection[level+1], None))
            edges[right_connection[level+1]].append((right_connection[level], None))
            del left_connection[level+1]
            del right_connection[level+1]
            #left_connection[level] = right_connection[level]
        else:
            if not regex[i] in ("|", "?", "*", "+"):
                edges[left_connection[level]].append((right_connection[level], regex[i]))
                if i == len(regex)-1 or (i < len(regex)-1 and not regex[i+1] == "|"):
                    edges.append([])
                    nodes_levels.append(level)
                    start_level[level] = left_connection[level]
                    left_connection[level] = right_connection[level]
                    right_connection[level] = len(edges)-1
            elif regex[i] == "?":
                edges[start_level[level]].append((right_connection[level], None))
            elif regex[i] == "*":
                edges[start_level[level]].append((right_connection[level], None))
                edges[right_connection[level]].append((start_level[level], None))
            elif regex[i] == "+":
                edges[right_connection[level]].append((start_level[level], None))
        i = i + 1

    j = 0
    found = False
    while j < len(edges[left_connection[0]]):
        if edges[left_connection[0]][j][0] == right_connection[0]:
            found = True
            break
        j = j + 1

    if not found:
        edges[left_connection[0]].append((right_connection[0], None))
        pass

    return edges, 0, right_connection[0]


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

gg, start_node, end_node = parse(" a(b|(c|(de)))*f ")
#gg, start_node, end_node = parse(" abcdefg* ")
view_gg(gg)
print(len(gg))
print(start_node)
print(end_node)
