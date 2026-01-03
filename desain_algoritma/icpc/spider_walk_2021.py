# spider walk 2021  
def spider_walk(n, m, grid):
    from collections import deque

    # Directions for moving up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Find the starting position of the spider (S)
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j)
            if grid[i][j] == 'E':
                end = (i, j)

    # BFS to find the shortest path from S to E
    queue = deque([start])
    visited = set()
    visited.add(start)
    distance = {start: 0}

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            return distance[(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                distance[(nx, ny)] = distance[(x, y)] + 1
                queue.append((nx, ny))

    return -1  # Return -1 if there is no path from S to E

# what is the time complexity of this algorithm?
# The time complexity of the spider_walk algorithm is O(n * m), 
# where n is the number of rows and m is the number of columns in the grid.
# This is because, in the worst case, we may need to visit every cell in the grid once during the breadth-first search (BFS) traversal. 
# Each cell is processed in constant time, leading to a total time complexity proportional to the number of cells in the grid.

# The first line of input has three integers n, m, and s, where n (3 ≤ n ≤ 200 000) is the number of
# strands, m (0 ≤ m ≤ 500 000) is the number of bridges, and s (1 ≤ s ≤ n) is Charlotte’s favorite
# strand. Strands are labeled from 1 to n in counterclockwise order. Each of the remaining m lines
# contains two integers d and t describing a bridge, where d (1 ≤ d ≤ 109) is the bridge’s distance from
# the center of the spiderweb and t (1 ≤ t ≤ n) is the first strand of the bridge in counterclockwise order.
# Specifically, if 1 ≤ t < n, then the bridge connects strands t and t+1. If t = n, then the bridge connects
# strands 1 and n. All bridge distances d are distinct
# 7 5 6
# 2 1
# 4 3
# 6 3
# 8 7
# 10 