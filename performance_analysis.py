"""Benchmark runner comparing RBtree, BST, and AVL for insert/search/delete.

Usage:
    python3 performance_analysis.py

The script runs moderate-sized benchmarks, saves CSV summaries, and creates comparison plots.
"""
import time
import random
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys

from RBtree1 import RBtree
from bst import BST
from avl import AVL

# increase recursion limit so recursive deletes on degenerate BSTs don't crash the run
sys.setrecursionlimit(1000000)


def timed(func):
    t0 = time.perf_counter()
    func()
    return time.perf_counter() - t0


def benchmark_one_structure(name, ctor, sizes, distributions, trials=3, out_dir='perf_outputs'):
    os.makedirs(out_dir, exist_ok=True)
    summary_path = os.path.join(out_dir, f'summary_{name}.csv')
    with open(summary_path, 'w', newline='') as sfile:
        writer = csv.writer(sfile)
        writer.writerow(['distribution', 'n', 'trial', 'insert_time', 'search_time', 'delete_time'])

        for dist in distributions:
            for n in sizes:
                for trial in range(1, trials + 1):
                    # prepare values according to distribution
                    if dist == 'random':
                        values = list(range(n))
                        random.shuffle(values)
                    elif dist == 'sorted':
                        values = list(range(n))
                    elif dist == 'reversed':
                        values = list(range(n))[::-1]
                    else:
                        values = list(range(n))

                    ds = ctor()

                    # measure insertion of all values
                    insert_time = timed(lambda: [ds.insertInTree(v) for v in values])

                    # measure search: sample 100 targets (existing)
                    sample_search = random.choices(values, k=min(100, max(1, n)))
                    search_time = timed(lambda: [ds.searchTree(v) for v in sample_search])

                    # measure deletion: delete half of the elements chosen at random
                    to_delete = random.sample(values, k=min(len(values), max(1, len(values)//2)))
                    # run deletion in a try/except so a single structure's deletion error doesn't stop the full benchmark
                    try:
                        delete_time = timed(lambda: [ds.deleteFromTree(v) for v in to_delete])
                    except Exception as e:
                        # record NaN for failed deletion and continue
                        print(f"{name} | dist={dist} n={n} trial={trial} deletion raised {e}")
                        delete_time = float('nan')

                    writer.writerow([dist, n, trial, f"{insert_time:.12e}", f"{search_time:.12e}", f"{delete_time:.12e}"])
                    print(f"{name} | dist={dist} n={n} trial={trial} insert={insert_time:.6f}s search={search_time:.6f}s delete={delete_time:.6f}s")

    return summary_path


def aggregate_and_plot(output_dir='perf_outputs'):
    # read CSVs for each structure and plot insert/search/delete vs n for each distribution
    structures = ['RBtree', 'BST', 'AVL']
    files = {s: os.path.join(output_dir, f'summary_{s}.csv') for s in structures}

    distributions = ['random', 'sorted', 'reversed']
    metrics = ['insert_time', 'search_time', 'delete_time']

    for dist in distributions:
        plt.figure(figsize=(12, 8))
        for i, metric in enumerate(metrics, start=1):
            plt.subplot(3, 1, i)
            for s in structures:
                path = files[s]
                if not os.path.exists(path):
                    continue
                data = np.genfromtxt(path, delimiter=',', dtype=str, skip_header=1)
                # filter by distribution
                if data.size == 0:
                    continue
                if data.ndim == 1:
                    rows = np.array([data])
                else:
                    rows = data
                mask = rows[:, 0] == dist
                rows = rows[mask]
                if rows.size == 0:
                    continue
                ns = rows[:, 1].astype(int)
                vals = rows[:, 3 + (metrics.index(metric))].astype(float)
                # aggregate by n (average across trials)
                unique_ns = np.unique(ns)
                avg_vals = [np.mean(vals[ns == u]) for u in unique_ns]
                plt.plot(unique_ns, avg_vals, marker='o', label=f'{s}')
            plt.ylabel(metric)
            plt.xscale('log')
            plt.legend()
            plt.grid(True, ls='--', alpha=0.5)
        plt.suptitle(f'Benchmark: distribution={dist}')
        out_png = os.path.join(output_dir, f'comparison_{dist}.png')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(out_png)
        print(f"Saved plot: {out_png}")
        try:
            # try to show the plot non-blocking; in headless environments this may be a no-op
            plt.show(block=False)
            plt.pause(0.1)
        except Exception:
            pass
        finally:
            plt.close()


def main():
    random.seed(0)
    sizes = [100, 1000, 5000, 10000]
    distributions = ['random', 'sorted', 'reversed']
    trials = 3
    out_dir = 'perf_outputs'

    # Map names to constructors
    structures = [
        ('RBtree', RBtree),
        ('BST', BST),
        ('AVL', AVL),
    ]

    for name, ctor in structures:
        benchmark_one_structure(name, ctor, sizes, distributions, trials=trials, out_dir=out_dir)

    aggregate_and_plot(out_dir)


if __name__ == '__main__':
    main()
