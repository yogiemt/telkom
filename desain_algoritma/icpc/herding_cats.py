import sys

def main():
    input = sys.stdin.readline

    T = int(input())
    for _ in range(T):
        N, M = map(int, input().split())

        P = [0] * (N + 1)
        catn = [0] * (M + 1)
        plantn = [0] * (M + 1)
        plantpos = [0] * (M + 1)
        plantposn = [0] * (M + 1)
        like = [[] for _ in range(N + 1)]

        for cat in range(1, N + 1):
            row = list(map(int, input().split()))
            P[cat] = row[0]
            K = row[1]
            plants = row[2:]

            catn[P[cat]] += 1

            for plant in plants:
                like[cat].append(plant)
                if P[cat] > plantpos[plant]:
                    plantpos[plant] = P[cat]
                    plantposn[plant] = 1
                elif P[cat] == plantpos[plant]:
                    plantposn[plant] += 1

        fail = False

        for plant in range(1, M + 1):
            plantn[plantpos[plant]] += 1

        tot = 0
        for pos in range(M, 0, -1):
            tot += plantn[pos]
            if tot > M - pos + 1:
                fail = True

        for cat in range(1, N + 1):
            found = False
            for plant in like[cat]:
                if (
                    plantpos[plant] == P[cat]
                    and plantposn[plant] == catn[P[cat]]
                ):
                    found = True
                    break
            if not found:
                fail = True

        print("NO" if fail else "YES")


if __name__ == "__main__":
    main()
