import time
import random
import os
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from RBtree1 import RBtree


def run_search_suite():
    sizes = [100, 500, 1000, 2000, 5000]
    out_dir = 'search_outputs'
    os.makedirs(out_dir, exist_ok=True)

    avg_search_times = []
    avg_search_times_norm = []

    for n in sizes:
        # build tree with n unique values
        values = list(range(n))
        random.shuffle(values)
        tree = RBtree()
        for v in values:
            tree.insertInTree(v)

        # prepare search samples: half successful, half unsuccessful
        sample_size = min(1000, max(100, n))
        successful = random.choices(values, k=sample_size//2) if n > 0 else []
        unsuccessful = [n + i for i in range(sample_size - len(successful))]
        samples = successful + unsuccessful
        random.shuffle(samples)

        per_search = []
        csv_path = os.path.join(out_dir, f'search_per_n_{n}.csv')
        with open(csv_path, 'w', newline='') as csvf:
            writer = csv.writer(csvf)
            writer.writerow(['index', 'value', 'found', 'search_time_seconds'])
            for i, v in enumerate(samples, start=1):
                t0 = time.perf_counter()
                found = tree.searchTree(v)
                t1 = time.perf_counter()
                dt = t1 - t0
                per_search.append(dt)
                writer.writerow([i, v, int(bool(found)), f"{dt:.12e}"])
                # also print each search time concisely
                print(f"n={n}, search #{i}, value={v}, found={found}, time={dt:.12e}s")

        avg = float(np.mean(per_search)) if per_search else 0.0
        avg_search_times.append(avg)
        norm = avg / math.log2(n) if n > 1 else avg
        avg_search_times_norm.append(norm)

        print(f"n={n}: avg search {avg:.6e}s (norm {norm:.6e}) — per-search CSV: {csv_path}")

    # Plot average search time and normalized by log2(n)
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(sizes, avg_search_times, 'o-', label='Avg search time')
    ax.plot(sizes, avg_search_times_norm, 's--', label='Avg / log2(n)')
    ax.set_xlabel('Number of elements (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('RB-Tree Search Time (avg per-sample)')
    ax.legend()
    ax.grid(True)
    out_png = os.path.join(out_dir, 'rbtree_search_times.png')
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Saved search plot to: {out_png}")
    plt.show()


if __name__ == '__main__':
    random.seed(0)
    run_search_suite()
