def insertion_sort(arr):
    n = len(arr)
    i = 1
    while i < n:
        t = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > t:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = t
        i += 1

    print(arr)

arr = [5, 4, 3, 2, 1]
insertion_sort(arr)