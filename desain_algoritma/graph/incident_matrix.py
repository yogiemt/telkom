incident_matrix = [
    [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 1, 0, 2, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 2, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 2, 0, 0, 2]
]

def is_edge(IM, u, v):
    i = 0
    m = len(IM)
    while i < m and IM[u][i] and IM[v][i] != 2:
        i += 1

    return i <= m 


def list_neighbors(IM, v):
    neighbors = []
    n = len(IM)
    m = len(IM[0])
    for i in range(m):
        if IM[v][i] != 0:
            for j in range(n):
                if j != v and IM[j][i] != 0:
                    neighbors.append(j)
    
    return neighbors