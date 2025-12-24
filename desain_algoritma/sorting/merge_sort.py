def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r -m 
    
    l = [0] * n1
    r = [0] * n2

    for i in range(n1):
        l[i] = arr[l + i]
    
    for j in range(n2): 
        r[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l
    while i < n1 and j < n2:
        if l[i] <= r[j]:
            arr[k] = l[i]
            i += 1
        else:
            arr[k] = r[j]
            j += 1
        k += 1  

    while i < n1:
        arr[k] = l[i]
        i += 1
        k += 1  
    while j < n2:
        arr[k] = r[j]
        j += 1
        k += 1

def merge_sort(arr, l, r):
    if l < r:
        m = (l + r) // 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r) 