class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


nodeA = Node("A")
nodeB = Node("B")
nodeC = Node("C")
nodeD = Node("D")
nodeE = Node("E")
nodeF = Node("F")
nodeG = Node("G")
nodeH = Node("H")
nodeI = Node("I")

nodeE.next = nodeB

nodeE.next = nodeB
nodeF.next = nodeG
nodeG.next = nodeH
nodeH.next = nodeI

nodeA.next = nodeD
nodeD.next = nodeE


adj_list = {
    "A" : nodeD,
    "B" : nodeC,
    "C" : nodeD,
    "D" : nodeE,
    "E" : nodeF,
    "G" : None,
    "H" : nodeI,
    "I" : nodeA,
}

def isEdge(adj_list, v, u):
    p = adj_list[v]
    while p and p.val != u:
        p = p.next

    return p != None


def list_neighbors(adj_list, v):
    p = adj_list[v]
    neighbors= []
    while p:
        neighbors.append(p.val)
        p = p.next
    return neighbors


print(isEdge(adj_list,"E", "I"))
print(list_neighbors(adj_list, "E"))