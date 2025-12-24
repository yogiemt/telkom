graph = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0]
]


def isEdge(adj, v, u):
    return adj[v][u] == 1

def list_neighbors(adj, v):
    i = 0
    n = len(adj)
    neighbors = []
    while i < n:
        if adj[v][i] == 1:
            neighbors.append(i)
        i += 1
    return neighbors


print(isEdge(graph, 2, 3))

for i in range(len(graph)):
    print("{}: {},".format(i, list_neighbors(graph, i)))
