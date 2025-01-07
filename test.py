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
        n = 111 * (2**i)

        for test_type in results.keys():
            total_promotes_list = []

            for _ in range(20):  # Repeat 20 times
                total_promotes = 0
                tree = avl.AVLTree()

                # Generate arrays for this iteration
                if test_type == "sorted":
                    arr = [j for j in range(n)]  # ממוין
                elif test_type == "reverse_sorted":
                    arr = [j for j in range(n)][::-1]  # ממוין הפוך
                elif test_type == "random":
                    arr = create_random_array(n)  # אקראי
                elif test_type == "random_swap":
                    arr = random_swap([j for j in range(n)])  # החלפות אקראיות

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
        n = 111 * (2**i)  # Array size
        arr1 = [j for j in range(n)]  # ממוין (sorted)
        arr2 = arr1[::-1]             # ממוין הפוך (reverse sorted)
        

        # Initialize inversion counters for random and random_swap arrays
        random_inversions = []
        random_swap_inversions = []


        for _ in range(20): 
            arr3 = create_random_array(n)  # יצירת מערך אקראי
            arr4 = random_swap(arr1.copy())  # יצירת מערך ממוין עם החלפות אקראיות
 
            random_inversions.append(count_inversions_direct(arr3))
            random_swap_inversions.append(count_inversions_direct(arr4))

        # Count inversions for sorted and reverse sorted arrays (constant results)
        sorted_inversions = count_inversions_direct(arr1)  # תמיד 0
        reverse_sorted_inversions = count_inversions_direct(arr2)  # תמיד מקסימלי

        # Calculate averages for random and random_swap arrays
        avg_random_inversions = sum(random_inversions) / len(random_inversions)
        avg_random_swap_inversions = sum(random_swap_inversions) / len(random_swap_inversions)

        # Append results
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

    for i in range(1, 11):  # עד 10 = i
        n = 111 * (2 ** i)  # גודל המערך

        for test_type in results.keys():
            total_search_edges = []
            total_edges = 0

            for _ in range(20):  # להריץ 20 פעמים עבור כל סוג מערך
                # Generate arrays for this iteration
                if test_type == "sorted":
                    arr = [j for j in range(n)]  # ממוין
                elif test_type == "reverse_sorted":
                    arr = [j for j in range(n)][::-1]  # ממוין הפוך
                elif test_type == "random":
                    arr = create_random_array(n)  # אקראי
                elif test_type == "random_swap":
                    arr = random_swap([j for j in range(n)])  # החלפות אקראיות

                # Build the AVL tree and perform the search
                tree = avl.AVLTree()
                for var in arr:
                    
                    _, edges, _ = tree.finger_insert(var, "var")
                    if test_type == "sorted":
                        print(edges)
                    total_edges += edges

                total_search_edges.append(total_edges)

            # Compute the average edges traversed for this test type
            avg_edges = sum(total_search_edges) / len(total_search_edges)
            results[test_type].append((n, avg_edges))

    # Print results
    for test_type in results:
        print(f"\n{test_type.capitalize()} results:")
        for n, avg_edges in results[test_type]:
            print(f"Array size: {n}, Avg edges per search: {avg_edges:.2f}")

if __name__ == "__main__":
    #test_inversions()
    # test_insertions()
    test_search_edges()

  
    
