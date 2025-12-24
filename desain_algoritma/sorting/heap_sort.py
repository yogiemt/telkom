import heapq

def heap_sort(arr: list):
    heapq.heapify(arr)

    res = []

    while arr:
        min_val = heapq.heappop(arr)
        res.append(min_val)

    print(res)


if __name__ == '__main__':
    arr = [5, 4, 3, 2, 1]
    heap_sort(arr)

