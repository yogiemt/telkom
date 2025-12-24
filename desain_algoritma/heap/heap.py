class Heap:
    def __init__(self):
        pass

    def fix_downward(arr, p):
        n = len(arr)
        larger = p
        inprogress = True
        while inprogress:
            left = p * 2
            right = left + 1
            if left <= n and arr[left] > arr[larger]:
                larger = left
            
            if right <= n and arr[right] > arr[larger]:
                larger = right

            inprogress = p < larger
            if inprogress:
                arr[p], arr[larger] = arr[larger], arr[p]
                p = larger

    def fix_upward(arr, p):
        while p > 1 and arr[p // 2] <  arr[p]:
            arr[p], arr[p // 2] = arr[p // 2], arr[p]
            p = p // 2
        
    # def enqueue(arr, v)
    def contruct_heap(arr):
        i
