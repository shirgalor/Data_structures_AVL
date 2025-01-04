import random
import AVLTree as avl

def create_random_array(n):
    """Creates a random array of size n."""
    array = list(range(1, n + 1))
    random.shuffle(array)
    return array

def random_swap(array):
    """Performs random adjacent swaps on an array."""
    for i in range(len(array) - 1):
        if random.random() < 0.5:
            array[i], array[i + 1] = array[i + 1], array[i]
    return array

def count_inversions_direct(array):
    """Counts the number of inversions in the array directly (O(n^2))."""
    inversions = 0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                inversions += 1
    return inversions

def count_search_edges(tree, array):
    """Counts the total edges traversed during searches for all keys in the tree."""
    total_edges = 0
    for key in array:
        _, edges = tree.finger_search(key)  # Search for the key
        total_edges += edges

    return total_edges


def test_insertions():
    """Tests insertions and calculates average promotes."""
    results = {
        "sorted": [],
        "reverse_sorted": [],
        "random": [],
        "random_swap": []
    }

    for i in range(1, 11):  # עד 10 = i
        n = 111 * (2 ** i)
        arr1 = [j for j in range(n)]  # ממוין
        arr2 = arr1[::-1]            # ממוין הפוך
        arr3 = create_random_array(n)
        arr4 = random_swap(arr1.copy())

        for test_type, arr in zip(
            ["sorted", "reverse_sorted", "random", "random_swap"], 
            [arr1, arr2, arr3, arr4]
        ):
            total_promotes_list = []

            for _ in range(20):  # Repeat 20 times
                total_promotes = 0
                tree = avl.AVLTree()

                # Insert elements and count promotes
                for var in arr:
                    _, _, promotes = tree.finger_insert(var, "var")
                    total_promotes += promotes

                total_promotes_list.append(total_promotes)

            # Calculate average promotes across 20 experiments
            avg_promotes = sum(total_promotes_list) / len(total_promotes_list)
            results[test_type].append((n, avg_promotes))

    # Print results
    for test_type in results:
        print(f"\n{test_type.capitalize()} results:")
        for n, avg_promotes in results[test_type]:
            print(f"Array size: {n}, Avg promotes: {avg_promotes:.4f}")

def test_inversions():
    """Tests inversions and calculates averages."""
    results = {
        "sorted": [],
        "reverse_sorted": [],
        "random": [],
        "random_swap": []
    }

    for i in range(1, 6):  # עד 5 = i
        n = 111 * (2 ** i)
        arr1 = [j for j in range(n)]  # ממוין
        arr2 = arr1[::-1]            # ממוין הפוך

        random_inversions = []
        random_swap_inversions = []

        for _ in range(20):  # להריץ 20 פעמים
            arr3 = create_random_array(n)  # אקראי
            arr4 = random_swap(arr1.copy())  # החלפות אקראיות
            random_inversions.append(count_inversions_direct(arr3))
            random_swap_inversions.append(count_inversions_direct(arr4))

        sorted_inversions = count_inversions_direct(arr1)  # 0 תמיד
        reverse_sorted_inversions = count_inversions_direct(arr2)  # מקסימלי

        avg_random_inversions = sum(random_inversions) / len(random_inversions)
        avg_random_swap_inversions = sum(random_swap_inversions) / len(random_swap_inversions)

        results["sorted"].append((n, sorted_inversions))
        results["reverse_sorted"].append((n, reverse_sorted_inversions))
        results["random"].append((n, avg_random_inversions))
        results["random_swap"].append((n, avg_random_swap_inversions))

    # Print results
    for test_type in results:
        print(f"\n{test_type.capitalize()} results:")
        for n, avg_inversions in results[test_type]:
            print(f"Array size: {n}, Avg inversions: {avg_inversions:.2f}")

def test_search_edges():
    """Tests searches and calculates average edges traversed."""
    results = {
        "sorted": [],
        "reverse_sorted": [],
        "random": [],
        "random_swap": []
    }

    for i in range(1, 11):  
        n = 111 * (2 ** i)

        sorted_search_edges = []
        reverse_sorted_search_edges = []
        random_search_edges = []
        random_swap_search_edges = []

        for _ in range(20):  # Repeat 20 times for all arrays
            arr1 = [j for j in range(n)]  # ממוין
            arr2 = arr1[::-1]            # ממוין הפוך
            arr3 = create_random_array(n)  # אקראי
            arr4 = random_swap(arr1.copy())  # החלפות אקראיות

            tree_sorted = avl.AVLTree()
            for var in arr1:
                tree_sorted.finger_insert(var, "var")
            sorted_search_edges.append(count_search_edges(tree_sorted, arr1))

            tree_reverse_sorted = avl.AVLTree()
            for var in arr2:
                tree_reverse_sorted.finger_insert(var, "var")
            reverse_sorted_search_edges.append(count_search_edges(tree_reverse_sorted, arr2))

            tree_random = avl.AVLTree()
            for var in arr3:
                tree_random.finger_insert(var, "var")
            random_search_edges.append(count_search_edges(tree_random, arr3))

            tree_random_swap = avl.AVLTree()
            for var in arr4:
                tree_random_swap.finger_insert(var, "var")
            random_swap_search_edges.append(count_search_edges(tree_random_swap, arr4))

      # Compute the average edges per search correctly
        avg_sorted_search_edges = sum(sorted_search_edges) / len(sorted_search_edges)
        avg_reverse_sorted_search_edges = sum(reverse_sorted_search_edges) / len(reverse_sorted_search_edges)
        avg_random_search_edges = sum(random_search_edges) / len(random_search_edges)
        avg_random_swap_search_edges = sum(random_swap_search_edges) / len(random_swap_search_edges)

        # Append the results (no need to divide by `n` unless explicitly needed)
        results["sorted"].append((n, avg_sorted_search_edges))
        results["reverse_sorted"].append((n, avg_reverse_sorted_search_edges))
        results["random"].append((n, avg_random_search_edges))
        results["random_swap"].append((n, avg_random_swap_search_edges))

    # Print results
    for test_type in results:
        print(f"\n{test_type.capitalize()} results:")
        for n, avg_edges in results[test_type]:
            print(f"Array size: {n}, Avg edges per search: {avg_edges:.2f}")

if __name__ == "__main__":
    test_inversions()
    test_insertions()
    test_search_edges()
