import networkx as nx

pair_direction = {
    1: 0,
    14: 1,
    28: 2,
    13: 3,
    -1: 4,
    -15: 5,
    -28: 6,
    -14: 7
}

impair_direction = {
    1: 0,
    15: 1,
    28: 2,
    14: 3,
    -1: 4,
    -14: 5,
    -28: 6,
    -13: 7
}


def create_single_path(cell1, cell2, final=0):
    if not (cell1//14) % 2:
        direction = pair_direction
    else:
        direction = impair_direction
    if final:
        return (direction[cell2 - cell1] * 4096 + cell2), direction[cell2 - cell1]
    return (direction[cell2 - cell1] * 4096 + cell1), direction[cell2 - cell1]


def format_path(path=None):
    if not path: return path
    else:
        formatted_path = []
        oldoff = 500
        for i in range(len(path)-1):
            paths, off = create_single_path(path[i], path[i + 1])
            if off != oldoff:
                formatted_path.append(paths)
                oldoff = off
        formatted_path.append(create_single_path(path[-2], path[-1], 1)[0])
        return formatted_path


def create_graph(cells=range(560), diag_weight=.9, vertical_weight=1):
    g = nx.Graph()
    g.add_node(cells)
    for j in cells:
        pair1 = [j+1, j+28]
        pair2 = [j+14, j+13]
        impair1 = [j+1, j+28]
        impair2 = [j+15, j+14]
        if not (j // 14) % 2:
            if j % 14 == 0:
                pair1 = [j+1, j+28]
                pair2 = [j+14]
            elif (j + 1) % 14 == 0:
                pair1 = [j+28]
                pair2 = [j+13]
            g.add_edges_from([(j, i) for i in pair1 if (560 > i >= 0)], weight=vertical_weight)
            g.add_edges_from([(j, i) for i in pair2 if (560 > i >= 0)], weight=diag_weight)
        else:
            if j % 14 == 0:
                impair1 = [j + 1, j + 28]
                impair2 = [j + 15]
            if (j + 1) % 14 == 0:
                impair1 = [j + 28]
                impair2 = [j + 14]
            g.add_edges_from([(j, i) for i in impair1 if (560 > i >= 0)], weight=vertical_weight)
            g.add_edges_from([(j, i) for i in impair2 if (560 > i >= 0)], weight=diag_weight)
    return g


def shortest_path(graph, source, target):
    return format_path(nx.algorithms.shortest_paths.weighted.dijkstra_path(graph, source, target))


if __name__ == '__main__':
    g = create_graph()
    print(shortest_path(g, 419, 166))
