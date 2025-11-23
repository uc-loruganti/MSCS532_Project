import random
import string
import time
import tracemalloc
import csv
import os
from InventoryManager import InventoryManager
from Product import Product


def random_name(word_count=3):
    words = []
    for _ in range(word_count):
        length = random.randint(3, 10)
        words.append(''.join(random.choices(string.ascii_letters, k=length)))
    return ' '.join(words)


def generate_products(n):
    for i in range(n):
        sku = f"SKU{i:09d}"
        name = random_name(random.randint(2,4))
        price = round(random.uniform(5, 2000), 2)
        qty = random.randint(0, 1000)
        category = random.choice(['Electronics', 'Books', 'Home', 'Garden', 'Toys', 'Clothing'])
        yield Product(sku, name, price, qty, category)


def measure_for_N(N, store_nodes):
    random.seed(12345)
    mgr = InventoryManager(store_skus_in_trie=store_nodes)
    # generate products
    products = list(generate_products(N))

    tracemalloc.start()
    t0 = time.perf_counter()
    mgr.bulk_load(products)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    # do a prefix search for a likely common prefix: take first char of first product
    prefix = products[0].name[0]
    # cold lookup
    t2 = time.perf_counter()
    res = mgr.get_products_by_name_prefix(prefix, limit=50)
    t3 = time.perf_counter()
    # hot lookup
    t4 = time.perf_counter()
    res2 = mgr.get_products_by_name_prefix(prefix, limit=50)
    t5 = time.perf_counter()
    tracemalloc.stop()

    return {
        'N': N,
        'mode': 'node' if store_nodes else 'subtree',
        'build_time_s': t1 - t0,
        'mem_current_mb': current / 1024 / 1024,
        'mem_peak_mb': peak / 1024 / 1024,
        'cold_lookup_s': t3 - t2,
        'hot_lookup_s': t5 - t4,
        'found': len(res)
    }


def run(ns, out_csv='tests/metrics.csv'):
    fieldnames = ['N','mode','build_time_s','mem_current_mb','mem_peak_mb','cold_lookup_s','hot_lookup_s','found']
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for N in ns:
            for mode in (True, False):
                print(f"Running N={N} mode={'node' if mode else 'subtree'}")
                try:
                    row = measure_for_N(N, mode)
                except MemoryError:
                    print(f"MemoryError for N={N} mode={mode}")
                    continue
                writer.writerow(row)
                f.flush()


if __name__ == '__main__':
    # default sizes; adjust if needed
    sizes = [20000, 50000, 80000]
    run(sizes)
