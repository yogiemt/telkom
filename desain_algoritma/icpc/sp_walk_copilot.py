import sys

def get_input():
    # Reading the first line using your style
    line1 = input().strip().split()
    if not line1:
        return
    
    n = int(line1[0])
    m = int(line1[1])
    s = int(line1[2])

    bridges = []
    for _ in range(m):
        # Reading each bridge line using your style
        bridge_line = input().strip().split()
        if not bridge_line:
            continue
        d = int(bridge_line[0])
        t = int(bridge_line[1])
        bridges.append((d, t))

    return n, m , s, bridges

import sys

import sys


def solve(n, m, s, bridges):
    """
    n: number of positions (ring), positions are 1..n
    m: number of bridges
    s: spider ID whose distance to others we compute (1..n)
    bridges: list of (d, t) where t is a position (1..n) that swaps with t+1 (wrap n->1)
    """

    # Process bridges by descending d (change to ascending if the problem says so)
    bridges.sort(key=lambda x: -x[0])

    # pos_to_spider[p] = spider at position p (1..n), initialize identity
    pos_to_spider = list(range(n + 1))  # index 0 unused

    # Apply swaps in the chosen order
    for _, t1 in bridges:
        t2 = t1 + 1 if t1 < n else 1
        pos_to_spider[t1], pos_to_spider[t2] = pos_to_spider[t2], pos_to_spider[t1]

    # spider_final_pos[i] = final position (1..n) of spider i
    spider_final_pos = [0] * (n + 1)
    for p in range(1, n + 1):
        spider_final_pos[pos_to_spider[p]] = p

    # Position of spider s after all swaps
    s_pos = spider_final_pos[s]

    # Print circular distance from spider s to each spider i
    for i in range(1, n + 1):
        diff = abs(spider_final_pos[i] - s_pos)
        print(min(diff, n - diff))




def solve_cursor(n, m, s_pos, bridges):
    # descending by d
    bridges.sort(key=lambda x: -x[0])

    pos_to_spider = list(range(n + 1))  # 1..n

    for _, t1 in bridges:
        t2 = t1 + 1 if t1 < n else 1
        # swap spiders at positions
        pos_to_spider[t1], pos_to_spider[t2] = pos_to_spider[t2], pos_to_spider[t1]
        # move the cursor if it sits at a swapped position
        if s_pos == t1:
            s_pos = t2
        elif s_pos == t2:
            s_pos = t1

    # final mapping spider -> position
    spider_final_pos = [0] * (n + 1)
    for p in range(1, n + 1):
        spider_final_pos[pos_to_spider[p]] = p

    # print distances to the final cursor position
    for i in range(1, n + 1):
        diff = abs(spider_final_pos[i] - s_pos)
        print(min(diff, n - diff))


if __name__ == "__main__":
    n, m, s = 7, 5, 6
    bridges = [(2, 1), (4, 3), (6, 3), (8, 7), (10, 5)]
    solve_cursor(n, m, s, bridges)


# 7 5 6
# 2 1
# 4 3
# 6 3
# 8 7
# 10 5


# 2
# 1
# 1
# 1
# 0
# 1
# 2