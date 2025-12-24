def selection_sort(arr):
    len_arr = len(arr)
    for i in range(len_arr):
        min_idx = i
        for j in range(i, len_arr):
            if arr[j] < arr[min_idx]:
                curr_min_idx = j

        arr[i], arr[curr_min_idx] = arr[curr_min_idx], arr[i]
    
    print(arr)

arr = [1, 2, 3, 4, 5]
selection_sort(arr)
            