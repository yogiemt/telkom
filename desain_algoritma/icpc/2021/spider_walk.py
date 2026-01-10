
import bisect # for binary search operations

class SlopeRing:
    # time: O(N) init, O(log N) per apply_swap
    def __init__(self, N, S):
        self.N = N
        self.m = {}        # posisi -> slope
        self.keys = []     # kunci terurut (breakpoints)

        # Inisialisasi ring dengan posisi awal
        # s = S
        half = (S + N // 2) % N 
        half_next = (S + (N + 1) // 2) % N


        self.m = {
            S: 1, 
            half: 0,
            half_next: -1,
        }
        print("Initial slopes:", self.m)
        self.keys = sorted(self.m)
        print("Initial keys dari slopes:", self.keys)

    # --- Manajemen keys terpusat ---
    # time: O(log K +  K)
    def ensure_key(self, k):
        """Pastikan k ada di keys (terurut) jika m memiliki entri untuk k."""
        if k in self.m:
            pos = bisect.bisect_left(self.keys, k)
            if pos == len(self.keys) or self.keys[pos] != k:
                self.keys.insert(pos, k)

    # time: O(log K + K)
    def remove_key(self, k):
        """Hapus k dari m dan keys bila ada."""
        if k in self.m:
            del self.m[k]
            pos = bisect.bisect_left(self.keys, k)
            if pos < len(self.keys) and self.keys[pos] == k:
                self.keys.pop(pos)

    # Mengembalikan indeks predecessor (indeks sebelumnya) dari i dalam daftar self.keys, 
    # dengan sifat siklik (circular).
    def pred_idx(self, i):
        return (i - 1) % len(self.keys)

    # Mengembalikan indeks successor (indeks setelah i) dalam daftar self.keys, 
    # dengan sifat siklik (circular).
    def succ_idx(self, i):
        return (i + 1) % len(self.keys)

    # returns the index of the largest key <= x (cyclic).
    # time: O(log K)
    def pred_of_upper_bound(self, x):
        """Indeks dari kunci terakhir yang <= x (cyclic)."""
        ub = bisect.bisect_right(self.keys, x)
        return (ub - 1) % len(self.keys)

    # get neighbors of breakpoint x
    # time: O(log K)
    def get_neighbors(self, x):
        """
        Kembalikan indeks (left_idx, ctrl_idx, right_idx) ke self.keys:
          ctrl_idx  = predecessor of upper_bound(x)
          left_idx = ctrl_idx, kecuali keys[ctrl_idx] == x, maka mundur satu lagi
          right_idx = succ(ctrl_idx) hanya jika keys[right_idx] == (x+1)%N, selain itu right_idx = ctrl_idx
        """
        ctrl_idx  = self.pred_of_upper_bound(x)
        left_idx  = ctrl_idx 
        right_idx = self.succ_idx(ctrl_idx )

        if self.keys[left_idx] == x:
            left_idx = self.pred_idx(left_idx)

        # right_idx hanya relevan sebagai “tetangga kanan” jika memang ada breakpoint tepat di (x+1) % N.
        # Kalau tidak ada breakpoint di posisi itu, maka segmen kanan dari x masih dikendalikan oleh breakpoint yang sama dengan x (yaitu ctrl_idx)
        if self.keys[right_idx] != (x + 1) % self.N:
            right_idx = ctrl_idx 

        return left_idx, ctrl_idx , right_idx

    # --- Set slope dengan penggabungan breakpoint redundant ---
    def set_slope(self, x, d):
        print("self.m", self.m)
        print("self.keys", self.keys)
        pit, it, nit = self.get_neighbors(x)
        print(f"set_slope({x}, {d}): pit={self.keys[pit]}, it={self.keys[it]}, nit={self.keys[nit]}")
        xd = self.m[self.keys[it]]
        pd = self.m[self.keys[pit]]
        nd = self.m[self.keys[nit]]
        print(f"  slopes: pd={pd}, xd={xd}, nd={nd}")
        print()
        print()

        if xd == d:
            return

        # Kelola breakpoint di x
        if d == pd:
            self.remove_key(x)
        else:
            self.m[x] = d
            self.ensure_key(x)

        # Kelola breakpoint di (x+1)
        nxt = (x + 1) % self.N
        if nd == d:
            self.remove_key(nxt)
        else:
            self.m[nxt] = nd
            self.ensure_key(nxt)        

    # --- Operasi swap adjacent pada posisi x ---
    def apply_swap(self, x: int) -> None:
        """
        Apply an adjacent swap at position x (i.e., swap between x and (x+1) % N),
        updating the local slope representation in a minimal (breakpoint) form.

        This performs:
        1) Read local neighborhood slopes around x.
        2) Flip central slope (if non-zero) and compensate neighbors.
        3) Normalize extremes (+/-2) and, if still extreme, propagate one step further.
        4) Commit the updated slopes at (x-1), x, and (x+1) using set_slope()
            so redundant breakpoints are merged away.

        The logic is identical to the original version—only rewritten to be clearer.
        """
        # Locate the neighborhood indices in self.keys
        pit_idx, it_idx, nit_idx = self.get_neighbors(x)

        # Resolve positions (breakpoints) and their slope values once, with descriptive names
        pos_prev  = self.keys[pit_idx]  # breakpoint just before 'it'
        pos_here  = self.keys[it_idx]   # controller breakpoint for position x
        pos_next  = self.keys[nit_idx]  # breakpoint that may be exactly at (x+1)%N

        slope_here = self.m[pos_here]  # slope at position x
        slope_prev = self.m[pos_prev]  # slope just before x
        slope_next = self.m[pos_next]  # slope at or after (x+1) % N

        # No effect on flat (central slope = 0)
        if slope_here == 0:
            return

        # Flip the central slope and compensate neighbors
        slope_here = -slope_here
        slope_prev -= slope_here
        slope_next -= slope_here

        # Normalize “edge” extremes
        if slope_prev == 2:
            slope_prev -= 1
            slope_here += 1
        if slope_next == -2:
            slope_next += 1
            slope_here -= 1

        # Propagate corrections if still extreme on either side
        if slope_prev == -2:
            slope_prev += 1
            # push one step backwards using the predecessor of pit
            prev_of_prev_idx = self.pred_idx(pit_idx)
            prev_of_prev_pos = self.keys[prev_of_prev_idx]
            prev_of_prev_val = self.m[prev_of_prev_pos]
            self.set_slope((pos_prev + (self.N - 1)) % self.N, prev_of_prev_val - 1)

        if slope_next == 2:
            slope_next -= 1
            # push one step forwards using the successor of nit
            next_of_next_idx = self.succ_idx(nit_idx)
            next_of_next_pos = self.keys[next_of_next_idx]
            next_of_next_val = self.m[next_of_next_pos]
            self.set_slope(next_of_next_pos, next_of_next_val + 1)

        # Commit local updates at (x-1), x, and (x+1)
        self.set_slope((x + self.N - 1) % self.N, slope_prev)
        self.set_slope(x, slope_here)
        self.set_slope((x + 1) % self.N, slope_next)

# Get Input
def read_cases():
    """
    returns:
    N : int - number of strands
    M : int - number of bridges
    S : int - starting strand (1-based)
    bridges : list of tuples (D, T) - bridge bridges
    returns N, M, S, bridges
    """
    N, M, S = [int(x) for x in input().strip().split()]

    bridges = []
    for _ in range(M):
        D, T = [int(x) for x in input().strip().split()]
        bridges.append((D, T))

    return N, M, S, bridges


# Solve Case Logic
# O(M log M + M log K + N), where K is the number of breakpoints in the slope representation
def solve_case(N, M, S, bridges):
    """
    Menyelesaikan satu test case sesuai algoritma:
    - Sort bridge berdasarkan D menurun
    - Terapkan swap (apply_swap) pada ring
    - Perbarui cursor s jika swap menyentuhnya
    - Integrasi slope untuk menghasilkan ret
    Mengembalikan list string (baris output).
    """
    # Ubah S ke 0-based untuk kemudahan indexing
    fav_strand = S - 1

    # Siapkan bridge dengan (-D, T-1) agar sort menaik ≡ D menurun
    bridges = [(-D, T - 1) for (D, T) in bridges]

    # time O(M log M)
    bridges.sort()

    ring = SlopeRing(N, fav_strand)

    # s: cursor awal (bergerak jika swap mengenai s atau s+1)
    s = fav_strand

    # time O(M log K)
    for _, t in bridges:
        ring.apply_swap(t)
        print(f"After swap at {t}: keys={ring.keys}, slopes={ring.m}")
        # pergerakan cursor s mengikuti swap t & t+1
        if s == t:
            s = (s + 1) % N
        elif s == (t + 1) % N:
            s = t


    print("Final slopes:", ring.m)
    # Rekonstruksi hasil dengan integrasi slope sepanjang ring
    ret = [0] * N
    cur = 0
    d = 0
    for _ in range(N):
        ret[s] = cur
        if s in ring.m:
            d = ring.m[s] # slope di posisi s
        cur += d
        s = (s + 1) % N
        print("ret", ret)

    # Kembalikan sebagai list of str (sesuai format print baris per nilai)
    return list(map(str, ret))


def main():
    N, M, S, bridges = read_cases()
    # N, M, S, bridges = (7, 5, 6, [(2, 1), (4, 3), (6, 3), (8, 7), (10, 5)])
    result = solve_case(N, M, S, bridges)
    print()
    print("Result:", [int(i) for i in result])
    print("\n".join(result))

if __name__ == "__main__":
    main()
