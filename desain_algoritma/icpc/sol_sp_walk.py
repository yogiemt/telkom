from sortedcontainers import SortedDict


def solve_case(N, M, S, bridges):
    S -= 1
    bridges = [(-D, T - 1) for D, T in bridges]
    bridges.sort()

    # Ordered map: position -> delta
    m = SortedDict()
    m[S] = 1
    m[(S + N // 2) % N] = 0
    m[(S + (N + 1) // 2) % N] = -1

    def pred_key(k):
        idx = m.bisect_left(k) - 1
        if idx < 0:
            idx = len(m) - 1
        return m.iloc[idx]

    def succ_key(k):
        idx = m.bisect_right(k)
        if idx == len(m):
            idx = 0
        return m.iloc[idx]

    def getAll(x):
        it = pred_key(x)
        pit = it
        nit = succ_key(it)

        if pit == x:
            pit = pred_key(pit)

        if nit != (x + 1) % N:
            nit = it

        return pit, it, nit

    def set_val(x, d):
        pit, it, nit = getAll(x)
        xd = m[it]
        pd = m[pit]
        nd = m[nit]

        if xd == d:
            return

        if d == pd:
            m.pop(x, None)
        else:
            m[x] = d

        nx = (x + 1) % N
        if nd == d:
            m.pop(nx, None)
        else:
            m[nx] = nd

    def swp(x):
        pit, it, nit = getAll(x)
        xd = m[it]
        pd = m[pit]
        nd = m[nit]

        if xd == 0:
            return

        xd = -xd
        pd -= xd
        nd -= xd

        if pd == 2:
            pd -= 1
            xd += 1

        if nd == -2:
            nd += 1
            xd -= 1

        if pd == -2:
            pd += 1
            p2 = pred_key(pit)
            set_val((pit + N - 1) % N, m[p2] - 1)

        if nd == 2:
            nd -= 1
            n2 = succ_key(nit)
            set_val(n2, m[n2] + 1)

        set_val((x + N - 1) % N, pd)
        set_val(x, xd)
        set_val((x + 1) % N, nd)

    s = S
    for _, t in bridges:
        swp(t)
        if s == t:
            s = (s + 1) % N
        elif s == (t + 1) % N:
            s = t

    ret = [0] * N
    cur = 0
    d = 0

    for _ in range(N):
        ret[s] = cur
        if s in m:
            d = m[s]
        cur += d
        s = (s + 1) % N

    return ret



def main():
    # 🔒 Hardcoded sample input
    N = 7
    M = 5
    S = 6
    bridges = [
        (2, 1),
        (4, 3),
        (6, 3),
        (8, 7),
        (10, 5),
    ]

    ans = solve_case(N, M, S, bridges)
    for x in ans:
        print(x)


if __name__ == "__main__":
    main()


