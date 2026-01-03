import sys
import bisect

def main():
    # Baca seluruh input sebagai deretan integer
    data = list(map(int, sys.stdin.read().split()))
    idx = 0
    out_lines = []

    # Loop setiap test case sampai kehabisan data
    while idx + 3 <= len(data):
        # Ambil N (ukuran ring), M (jumlah event), S (posisi awal, 1-based)
        N = data[idx]; M = data[idx + 1]; S = data[idx + 2]
        idx += 3
        S -= 1  # ubah ke 0-based (sesuai C++)

        # Baca M event sebagai tuple (-D, T-1) agar sort menaik ≡ D menurun
        b = []
        for _ in range(M):
            D = data[idx]
            T = data[idx + 1]
            idx += 2
            b.append((-D, T - 1))  # simpan D negatif + T 0-based
        b.sort()  # urutkan; ini membuat urutan D menurun

        # m: dict posisi -> slope (kemiringan lokal yang aktif mulai posisi itu)
        # keys: daftar posisi breakpoint terurut (untuk operasi siklik)
        m = {}
        keys = []

        # Helper: masukkan k ke keys (terurut) jika belum ada
        def insert_key(k):
            pos = bisect.bisect_left(keys, k)
            if pos == len(keys) or keys[pos] != k:
                keys.insert(pos, k)

        # Helper: hapus k dari m dan keys jika ada
        def erase_key(k):
            if k in m:
                del m[k]
                pos = bisect.bisect_left(keys, k)
                if pos < len(keys) and keys[pos] == k:
                    keys.pop(pos)

        # Inisialisasi breakpoint awal (seperti di C++):
        #   - slope +1 di S
        #   - slope  0 di titik berseberangan
        #   - slope -1 di posisi setelahnya (tetap siklik)
        m[S] = 1
        m[(S + N // 2) % N] = 0
        m[(S + (N + 1) // 2) % N] = -1
        keys = sorted(m.keys())  # pastikan keys sesuai isi m

        # Indeks predecessor/successor secara siklik pada keys
        def pred_index(i):
            return (i - 1) % len(keys)

        def succ_index(i):
            return (i + 1) % len(keys)

        # Cari indeks predecessor dari upper_bound(x):
        #   - upper_bound = indeks pertama kunci > x
        #   - predecessor upper_bound = kunci terakhir yang <= x (siklik)
        def pred_of_upper_bound(x):
            ub = bisect.bisect_right(keys, x)
            return (ub - 1) % len(keys)

        # Ambil lingkungan lokal di sekitar posisi x:
        #   - it: indeks breakpoint yang mengontrol slope di x (<= x)
        #   - pit: indeks breakpoint sebelumnya (kalau it persis di x, mundur lagi)
        #   - nit: indeks breakpoint berikutnya hanya bila kuncinya tepat (x+1)%N,
        #          jika tidak, nit disamakan dengan it (artinya slope di x+1 sama seperti di x)
        def getAll(x):
            it = pred_of_upper_bound(x)
            pit = it
            nit = succ_index(it)

            if keys[pit] == x:
                pit = pred_index(pit)
            if keys[nit] != (x + 1) % N:
                nit = it

            return pit, it, nit

        # Set slope di x menjadi d, dengan menjaga struktur breakpoint tetap "minimal":
        #   - jika slope di x sama dengan d, tidak ada perubahan
        #   - jika d sama dengan slope predecessor (pd), breakpoint di x redundan -> hapus
        #   - hal serupa diterapkan ke (x+1)%N terhadap slope nd
        def _set(x, d):
            pit, it, nit = getAll(x)
            xd = m[keys[it]]   # slope aktif pada x (diambil dari it)
            pd = m[keys[pit]]  # slope pada breakpoint sebelumnya
            nd = m[keys[nit]]  # slope pada breakpoint berikutnya (jika tepat di x+1), atau sama seperti it

            # Jika slope aktif sudah bernilai d, tidak perlu mengubah apa pun
            if xd == d:
                return

            # Jika d sama dengan slope predecessor, breakpoint di x tak diperlukan
            if d == pd:
                erase_key(x)
            else:
                # Simpan slope baru di x dan pastikan x ada di keys
                m[x] = d
                insert_key(x)

            # Untuk posisi (x+1)%N: jika slope-nya (nd) sama dengan d, hapus breakpoint di sana
            # else pertahankan/insert agar keys tetap konsisten
            nxt = (x + 1) % N
            if nd == d:
                erase_key(nxt)
            else:
                m[nxt] = nd
                insert_key(nxt)

        # Operasi swap adjacent pada posisi x (menukar x dengan x+1 di ring),
        # direpresentasikan sebagai pembalikan slope lokal dan penyeimbangan tetangga
        def _swp(x):
            pit, it, nit = getAll(x)
            xd = m[keys[it]]    # slope di x (aktif)
            pd = m[keys[pit]]   # slope di breakpoint sebelumnya
            nd = m[keys[nit]]   # slope di breakpoint berikutnya (jika tepat di x+1), atau sama seperti it

            # Jika slope di x adalah 0 (datar), swap tidak mengubah apa-apa
            if xd == 0:
                return

            # Balik slope pusat dan kompensasi tetangga:
            #   - membalik xd mencerminkan efek swap pada selisih lokal
            #   - pd dan nd dikurangi xd untuk menyeimbangkan transisi
            xd = -xd
            pd -= xd
            nd -= xd

            # Batasi ekstrem tetangga: jika melebihi rentang normal, kembalikan sebagian ke xd
            if pd == 2:
                pd -= 1
                xd += 1
            if nd == -2:
                nd += 1
                xd -= 1

            # Jika masih ekstrem, propagasikan koreksi ke breakpoint yang lebih jauh:
            #   - pd == -2: dorong koreksi satu langkah ke belakang
            if pd == -2:
                pd += 1
                prev_pit = pred_index(pit)
                prev_key = keys[prev_pit]
                prev_val = m[prev_key]
                _set((keys[pit] + (N - 1)) % N, prev_val - 1)

            #   - nd == 2: dorong koreksi satu langkah ke depan
            if nd == 2:
                nd -= 1
                next_nit = succ_index(nit)
                next_key = keys[next_nit]
                next_val = m[next_key]
                _set(next_key, next_val + 1)

            # Commit perubahan lokal di tiga titik: (x-1), x, (x+1) (mod N),
            # menggunakan _set agar breakpoint redundant otomatis dibersihkan
            _set((x + N - 1) % N, pd)
            _set(x, xd)
            _set((x + 1) % N, nd)

        # s: posisi awal (yang bisa bergeser jika swap mengenai s atau s+1)
        s = S
        for _, t in b:
            _swp(t)
            # Jika s berada di salah satu dari dua indeks yang ditukar, ikut bergeser
            if s == t:
                s = (s + 1) % N
            elif s == (t + 1) % N:
                s = t

        # Rekonstruksi nilai final ret dengan "mengintegrasikan" slope keliling ring
        ret = [0] * N
        cur = 0  # nilai kumulatif yang akan ditulis ke ret
        d = 0    # slope aktif saat ini
        for _ in range(N):
            ret[s] = cur        # tulis nilai kumulatif di posisi s
            if s in m:
                d = m[s]        # jika s adalah breakpoint, update slope aktif
            cur += d            # naikkan nilai kumulatif sesuai slope
            s = (s + 1) % N     # maju ke posisi berikutnya secara siklik

        # Tulis hasil sebagai baris-baris angka (sesuai format C++)
        for x in ret:
            out_lines.append(str(x))

    # Cetak seluruh output untuk semua test case
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()