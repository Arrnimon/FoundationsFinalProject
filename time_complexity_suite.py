import time
import random
import csv
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from RBtree1 import RBtree

def plot_complexity():
    sizes = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000]
    insert_times = []            # average time per insert for each n
    insert_times_norm = []       # average time per insert divided by log2(n)
    search_times = []
    
    for n in sizes:
        values = list(range(n))
        random.shuffle(values)

        # Measure per-insert times (inserting one at a time)
        tree = RBtree()
        per_insert_times = []
        for i, val in enumerate(values, start=1):
            t0 = time.perf_counter()
            tree.insertInTree(val)
            t1 = time.perf_counter()
            per_insert_times.append(t1 - t0)

        avg_per_insert = float(np.mean(per_insert_times)) if per_insert_times else 0.0
        insert_times.append(avg_per_insert)
        # normalize by log2(n) to see O(log n) behavior per insert
        norm = float(avg_per_insert / np.log2(n)) if n > 1 else avg_per_insert
        insert_times_norm.append(norm)
        # print a small sample of per-insert times for inspection
        sample_count = min(10, len(per_insert_times))
        sample_times = per_insert_times[:sample_count]
        print(f"n={n}: avg per-insert {avg_per_insert:.6e}s, sample first {sample_count} inserts: {', '.join(f'{t:.3e}' for t in sample_times)}")

        # Measure search time for a single random existing value
        if n > 0:
            target = random.choice(values)
            start = time.time()
            tree.searchTree(target)
            single_search_time = time.time() - start
        else:
            single_search_time = 0.0
        search_times.append(single_search_time)
        print(f"n={n}: single search time {single_search_time:.6e} seconds")
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Average per-insert time vs n
    ax1.plot(sizes, insert_times, 'bo-', label='Avg per-insert (measured)')
    # Also plot avg per-insert divided by log2(n) to inspect O(log n)
    ax1.plot(sizes, insert_times_norm, 'go-', label='Avg per-insert / log2(n)')
    ax1.set_xlabel('Number of elements (n)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Average Per-Insert Time (and normalized by log2(n))')
    ax1.legend()
    ax1.grid(True)
    
    # Search time vs n (log scale)
    ax2.plot(sizes, search_times, 'go-', label='Measured')
    # Compare to O(log n)
    theoretical_search = [np.log2(n) / 1000000 for n in sizes]  # Scaled
    ax2.plot(sizes, theoretical_search, 'r--', label='O(log n) theoretical')
    ax2.set_xlabel('Number of elements (n)')
    ax2.set_ylabel('Average time per search (seconds)')
    ax2.set_title('Search Time Complexity')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('rbtree_complexity.png')
    plt.show()

if __name__ == '__main__':
    plot_complexity()