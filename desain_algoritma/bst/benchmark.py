import two_three
import avltree
import treaps
import time
import matplotlib.pyplot as plt 
import json
from read_black import RedBlackTree


def benchmark_treap_operations():
    # data = [10, 100, 1000]
    data = [10, 100, 1000, 10000, 100000, 1000000, 10_000_000]
    time_results = {
        "treaps" : [],
        "two_three": [],
        "avl": [],
        "red_black": []
    }
    
    for n in data:
        start = time.time()

        treap = treaps.TreapNode(1, 1)

        for i in range(1, n):
            treap = treap.insert_node(i, priority=i)
        end = time.time()
        time_results["treaps"].append(end - start)

    print("treaps done")
    
    for n in data:
        start = time.time()

        two_three_tree = two_three.TwoTreeNode(1)

        for i in range(1, n):
            two_three_tree.insert(i)
        end = time.time()
        time_results["two_three"].append(end - start)

    print("two_three done")

    for n in data:
        start = time.time()

        avl_tree = avltree.AVLTree()
        for i in range(1, n):
            avl_tree.insert_value(i)

        end = time.time()
        time_results["avl"].append(end - start)

    print("avl done")

    for n in data:
        start = time.time()


        red_black_tree = RedBlackTree()
        for i in range(1, n):
            red_black_tree.insert(i)

        end = time.time()
        time_results["red_black"].append(end - start)

    print("red_black done")

    print("Benchmark Results:", json.dumps(time_results, indent=4))


    # create graph
    plt.plot(data, time_results["treaps"], label="Treaps")
    plt.plot(data, time_results["two_three"], label="2-3 Tree")
    plt.plot(data, time_results["avl"], label="AVL Tree")
    plt.plot(data, time_results["red_black"], label="Red-Black Tree")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Benchmark of Tree Insertion Operations")
    plt.legend()

    plt.savefig("benchmark_trees_2.png")
    plt.show()

if __name__ == "__main__":
    benchmark_treap_operations()