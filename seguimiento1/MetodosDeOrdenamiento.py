class MetodosDeOrdenamiento:
    # 1. TimSort (O(n log n) en el mejor y peor caso)
    def tim_sort(self, arr):
        arr.sort()
        print(arr)
        return arr

    # 2. Comb Sort (O(n^2) en el peor caso, O(n log n) en el mejor caso)
    def comb_sort(self, arr):
        gap = len(arr)
        shrink = 1.3
        sorted = False
        while not sorted:
            gap = int(gap // shrink)
            if gap <= 1:
                gap = 1
            sorted = True
            for i in range(len(arr) - gap):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted = False
        return arr

    # 3. Selection Sort (O(n^2))
    def selection_sort(self, arr):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    # 4. Tree Sort (O(n log n))
    class Node:
        def __init__(self, key):
            self.left = None
            self.right = None
            self.val = key

    def insert(self, root, key):
        if root is None:
            return self.Node(key)
        else:
            if key < root.val:
                root.left = self.insert(root.left, key)
            else:
                root.right = self.insert(root.right, key)
        return root

    def inorder_traversal(self, root, res):
        if root:
            self.inorder_traversal(root.left, res)
            res.append(root.val)
            self.inorder_traversal(root.right, res)

    def tree_sort(self, arr):
        if len(arr) == 0:
            return []
        root = self.Node(arr[0])
        for i in range(1, len(arr)):
            self.insert(root, arr[i])
        res = []
        self.inorder_traversal(root, res)
        return res

    # 5. Pigeonhole Sort (O(n + range))
    def pigeonhole_sort(self, arr):
        min_val = min(arr)
        max_val = max(arr)
        size = max_val - min_val + 1
        holes = [0] * size
        for x in arr:
            holes[x - min_val] += 1
        sorted_arr = []
        for i in range(size):
            while holes[i] > 0:
                sorted_arr.append(i + min_val)
                holes[i] -= 1
        return sorted_arr

    # 6. BucketSort (O(n + k))
    def bucket_sort(self, arr):
        if len(arr) == 0:
            return arr
        # Crear buckets
        bucket_count = 10  # Número de cubos
        max_value = max(arr)
        buckets = [[] for _ in range(bucket_count)]
        for number in arr:
            index = int(number / (max_value / bucket_count))
            if index >= bucket_count:  # Manejar el caso máximo
                index = bucket_count - 1
            buckets[index].append(number)
        # Ordenar cada cubo
        sorted_array = []
        for bucket in buckets:
            sorted_array.extend(sorted(bucket))  # Usar el método sort para ordenar
        return sorted_array

    # 7. QuickSort (O(n log n) en promedio, O(n^2) en el peor caso)
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    # 8. HeapSort (O(n log n))
    def heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def heap_sort(self, arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, i, 0)
        return arr

    # 9. Bitonic Sort (O(log^2 n))
    def bitonic_merge(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                if (direction == 1 and arr[i] > arr[i + k]) or (direction == 0 and arr[i] < arr[i + k]):
                    arr[i], arr[i + k] = arr[i + k], arr[i]
            self.bitonic_merge(arr, low, k, direction)
            self.bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(self, arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            self.bitonic_sort_recursive(arr, low, k, 1)
            self.bitonic_sort_recursive(arr, low + k, k, 0)
            self.bitonic_merge(arr, low, cnt, direction)

    def bitonic_sort(self, arr):
        self.bitonic_sort_recursive(arr, 0, len(arr), 1)
        return arr

    # 10. Gnome Sort (O(n^2))
    def gnome_sort(self, arr):
        index = 0
        while index < len(arr):
            if index == 0 or arr[index] >= arr[index - 1]:
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                index -= 1
        return arr

    # 11. Binary Insertion Sort (O(n^2))
    def binary_insertion_sort(self, arr):
        def binary_search(arr, val, start, end):
            if start == end:
                return start if arr[start] > val else start + 1
            if start > end:
                return start
            mid = (start + end) // 2
            if arr[mid] < val:
                return binary_search(arr, val, mid + 1, end)
            elif arr[mid] > val:
                return binary_search(arr, val, start, mid - 1)
            else:
                return mid

        for i in range(1, len(arr)):
            val = arr[i]
            j = binary_search(arr, val, 0, i - 1)
            arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]
        return arr

    #12.radix_sort
    def counting_sort(self, arr, exp):
        n = len(arr)
        output = [0] * n  # Array de salida
        count = [0] * 10  # Array para contar los dígitos

        # Contar la ocurrencia de los dígitos
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        # Cambiar count[i] para que contenga la posición final de este dígito en output[]
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Construir el array de salida
        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        # Copiar el array de salida a arr[], de modo que arr ahora esté ordenado según el dígito actual
        for i in range(len(arr)):
            arr[i] = output[i]

    # Método principal para radix_sort
    def radix_sort(self, arr):
        # Encontrar el número máximo para conocer la cantidad de dígitos
        max_num = max(arr)
        
        # Aplicar counting sort para cada dígito
        exp = 1
        while max_num // exp > 0:
            self.counting_sort(arr, exp)
            exp *= 10

        return arr
    


        