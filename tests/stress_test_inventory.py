import random
import string
import time
import tracemalloc
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
        sku = f"SKU{i:07d}"
        name = random_name(random.randint(2,4))
        price = round(random.uniform(5, 2000), 2)
        qty = random.randint(0, 1000)
        category = random.choice(['Electronics', 'Books', 'Home', 'Garden', 'Toys', 'Clothing'])
        yield Product(sku, name, price, qty, category)


def measure(build_mode_store_nodes: bool, n=20000, prefix='A'):
    print(f"\n=== Mode store_nodes={build_mode_store_nodes} N={n} ===")
    tracemalloc.start()
    t0 = time.perf_counter()
    mgr = InventoryManager(store_skus_in_trie=build_mode_store_nodes)
    # bulk load for faster construction
    products = list(generate_products(n))
    mgr.bulk_load(products)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Build time: {t1 - t0:.3f}s, current_mem={current/1024/1024:.2f}MB peak={peak/1024/1024:.2f}MB")

    # measure prefix search cold
    t2 = time.perf_counter()
    res = mgr.get_products_by_name_prefix(prefix, limit=50)
    t3 = time.perf_counter()
    print(f"Prefix search (cold) time: {t3 - t2:.4f}s, found={len(res)}")

    # measure prefix search hot (cached)
    t4 = time.perf_counter()
    res2 = mgr.get_products_by_name_prefix(prefix, limit=50)
    t5 = time.perf_counter()
    print(f"Prefix search (hot) time: {t5 - t4:.6f}s")

    tracemalloc.stop()


if __name__ == '__main__':
    random.seed(12345)
    # choose prefix as first letter of some generated name; using 'A' may match few
    # run for two modes for comparison
    measure(True, n=20000, prefix='A')
    measure(False, n=20000, prefix='A')
    print('\nStress test completed. Adjust N to scale higher.\n')
