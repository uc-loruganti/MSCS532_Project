from Product import Product
from TrieNode import Trie


# Small Trie used for caching prefix query results (case-insensitive keys)
class _PrefixCacheNode:
    def __init__(self):
        self.children: dict[str, _PrefixCacheNode] = {}
        self.cached_skus: list[str] | None = None

# Trie structure for caching prefix query results (case-insensitive keys)
# Each node may store a cached list of SKUs for the prefix leading to that node. So the key
# "App" would be stored by traversing 'A' -> 'p' -> 'p' nodes, and the last node would have
# cached_skus set to the list of SKUs matching that prefix.
class PrefixCacheTrie:
    def __init__(self):
        self.root = _PrefixCacheNode()

    def _normalize(self, key: str) -> str:
        return key.lower()

    def get(self, prefix: str) -> list[str] | None:
        node = self.root
        for ch in self._normalize(prefix):
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node.cached_skus

    def set(self, prefix: str, skus: list[str]):
        node = self.root
        for ch in self._normalize(prefix):
            node = node.children.setdefault(ch, _PrefixCacheNode())
        node.cached_skus = list(skus)

    def invalidate_prefixes_of_name(self, name: str):
        """Invalidate cached entries for all prefixes of the given name.

        For name 'Apple iPhone' this clears cached entries for 'a','ap','app',...
        The operation is O(m) where m is len(name).
        """
        node = self.root
        for ch in self._normalize(name):
            if ch not in node.children:
                return
            node = node.children[ch]
            node.cached_skus = None

    def clear(self):
        self.root = _PrefixCacheNode()


# Inventory Manager class definition for managing products.
# Uses multiple data structures for efficient operations. 
# 1. Primary Hash Table for SKU to Product mapping.
# 2. Category Index for category-based retrieval.
# 3. Search Trie for fast name-based retrieval.
class InventoryManager: 
    def __init__(self, store_skus_in_trie: bool = True): 
        # 1. Primary Hash Table
        self.products: dict[str, Product] = {}
        # 2. Category Index. Dictionary mapping category to set of SKUs
        self.categories: dict[str, set[str]] = {}
        # 3. Search Trie - configurable memory/time tradeoff
        self.search_trie = Trie(store_skus_in_nodes=store_skus_in_trie)
        # Prefix cache (Trie-backed) for case-insensitive prefix queries
        self._prefix_cache = PrefixCacheTrie()
        # Category cache: maps category -> list of SKUs
        self._category_cache: dict[str, list[str]] = {}

    # This function populates the inventory with sample data for testing
    def populate_sample_data(self):
        sample_products = [
            Product("SKU001", "Apple iPhone 13", 799.99, 50, "Electronics"),
            Product("SKU002", "Samsung Galaxy S21", 699.99, 30, "Electronics"),
            Product("SKU003", "Sony WH-1000XM4 Headphones", 349.99, 20, "Audio"),
            Product("SKU004", "Dell XPS 13 Laptop", 999.99, 15, "Computers"),
            Product("SKU005", "Apple MacBook Pro", 1299.99, 10, "Computers"),
            Product("SKU006", "Bose QuietComfort Earbuds", 279.99, 25, "Audio"),
            Product("SKU007", "Google Pixel 6", 599.99, 40, "Electronics"),
            Product("SKU008", "HP Spectre x360", 1099.99, 12, "Computers"),
            Product("SKU009", "JBL Flip 5 Speaker", 119.99, 35, "Audio"),
            Product("SKU010", "OnePlus 9 Pro", 729.99, 28, "Electronics"),
        ]
        for product in sample_products:
            self.add_product(product)

    # Function to add a new product to the inventory
    # This function updates all data structures accordingly
    # 1 : Add to primary hash table
    # 2 : Update category index
    # 3 : Update search trie
    def add_product(self, product: Product): 
        # Add product to primary hash table if not already present
        if product.sku in self.products:
            print(f"Product with SKU {product.sku} already exists. Please update instead of adding.")
            return
        self.products[product.sku] = product

        # Update category index with the new sku
        if product.category not in self.categories:
            self.categories[product.category] = set()
        self.categories[product.category].add(product.sku)

        # Update search trie (store lowercase names to make searches case-insensitive)
        name_norm = product.name.lower()
        self.search_trie.insert(name_norm, product.sku)
        # Invalidate prefix cache entries affected by this product's name because of new addition . This ensures correctness.
        self._prefix_cache.invalidate_prefixes_of_name(name_norm)
        # Invalidate category cache for this product's category
        self._category_cache.pop(product.category, None)

    # Function to remove a product from the inventory
    # This function updates all data structures accordingly
    # 1 : Remove from primary hash table
    # 2 : Remove from category index
    # 3 : Remove from search trie
    def remove_product(self, product: Product | str):
        """Remove a product by Product instance or SKU string."""
        sku = product.sku if isinstance(product, Product) else product
        prod = self.products.get(sku)
        if not prod:
            return

        # Remove from primary hash table
        del self.products[sku]

        # Remove from category index
        if prod.category in self.categories:
            self.categories[prod.category].discard(sku)
            if not self.categories[prod.category]:
                del self.categories[prod.category]

        # Remove from search trie (names stored normalized)
        self.search_trie.delete(prod.name.lower(), sku)
        # Invalidate prefix cache entries affected by this product's name
        self._prefix_cache.invalidate_prefixes_of_name(prod.name)
        # Invalidate category cache for this product's category
        self._category_cache.pop(prod.category, None)

    def remove_product_by_sku(self, sku: str):
        """Convenience method to remove by SKU."""
        self.remove_product(sku)


    # Update quantity of a product and other data structures if needed
    # Time complexity : O(1)
    # Space complexity : O(1)
    def update_quantity(self, sku: str, quantity: int): 
        product = self.get_product_by_sku(sku)
        if(product is None):
            print(f"Product with SKU {sku} does not exist.")
            return
        
        if(quantity < 0):
            print("Quantity cannot be negative.")
            return
        
        product.quantity = quantity
        self.products[product.sku] = product
        
        
    # Retrieve a product by its SKU
    # Return None if not found
    def get_product_by_sku(self, sku : str): 
        # O(1) lookup in primary hash table
        return self.products.get(sku, None)

    # Retrieve products by category
    # Time complexity : O(1) + O(n)
    # where n is number of products in that category
    # Space complexity : O(n) for the returned list
    def get_products_by_category(self, category: str):
        # O(1) lookup in category index
        if category in self.categories:
            # use category cache if available
            cached = self._category_cache.get(category)
            if cached is not None:
                return [self.products[sku] for sku in cached]
            skus = list(self.categories[category])
            self._category_cache[category] = list(skus)
            return [self.products[sku] for sku in skus]
        return []

    # Retrieve products by name prefix using the search trie
    # Time complexity : O(m) + O(n)
    # where m is length of the prefix and n is number of matching products
    # Space complexity : O(n) for the returned list
    def get_products_by_name_prefix(self, prefix: str, limit: int | None = None, as_generator: bool = False):
        """Retrieve products matching a name prefix.

        - `limit` optionally limits the number of returned products.
        - `as_generator=True` returns a generator that yields Product objects
          lazily (useful for very large result sets).
        This method employs a simple cache for repeated prefix queries; the
        cache is cleared on any inventory mutation.
        """
        # normalize prefix to lower-case for case-insensitive caching/search
        key = prefix.lower()
        skus = self._prefix_cache.get(key)
        if skus is not None:
            skus = list(skus)
        else:
            skus = list(self.search_trie.search(key))
            # populate prefix cache trie node for this prefix
            self._prefix_cache.set(key, skus)

        if limit is not None:
            skus = skus[:limit]

        if as_generator:
            def gen():
                for sku in skus:
                    yield self.products[sku]
            return gen()

        return [self.products[sku] for sku in skus]

    # Get all categories in the inventory
    # Time complexity : O(1)
    # Space complexity : O(n) for the returned list
    def get_categories(self):
        return list(self.categories.keys())

    def bulk_load(self, products_iterable):
        """Efficiently load many products.

        This replaces the existing data structures with ones built from the
        provided iterable. This is faster than calling `add_product` repeatedly
        because it avoids repeated cache clears and incremental trie updates.
        """
        # rebuild primary dict
        self.products = {p.sku: p for p in products_iterable}

        # rebuild categories
        self.categories = {}
        for p in self.products.values():
            self.categories.setdefault(p.category, set()).add(p.sku)

        # rebuild trie from scratch (faster than many incremental inserts in some modes)
        self.search_trie = Trie(store_skus_in_nodes=self.search_trie.store_skus_in_nodes)
        for p in self.products.values():
            # insert normalized (lowercase) names into the search trie
            self.search_trie.insert(p.name.lower(), p.sku)

        # reset cache
        self._prefix_cache.clear()

    def update_product_name(self, sku: str, new_name: str) -> bool:
        """Rename a product (update its name) while updating indexes/cache.

        This updates the primary product record, removes the old name from the
        trie, inserts the new name, and invalidates cached prefixes for both
        the old and the new name so queries remain correct.
        Returns True if update succeeded, False if SKU not found or name
        unchanged.
        """
        product = self.get_product_by_sku(sku)
        if not product:
            return False
        old_name = product.name
        if old_name == new_name:
            return True

        # Update trie: remove old name mapping and add new name mapping (normalized)
        self.search_trie.delete(old_name.lower(), sku)
        self.search_trie.insert(new_name.lower(), sku)

        # Update product record
        product.name = new_name
        self.products[sku] = product

        # Invalidate cache for prefixes affected by both old and new names
        self._invalidate_prefix_cache_for_name(old_name)
        self._invalidate_prefix_cache_for_name(new_name)
        return True

    def update_product_category(self, sku: str, new_category: str) -> bool:
        """Change a product's category and precisely invalidate caches.

        Updates the `categories` index, the product record, and invalidates
        the per-category cache entries for the old and new category only.
        Returns True if the update succeeded, False if the SKU was not found
        or if the category is unchanged.
        """
        product = self.get_product_by_sku(sku)
        if not product:
            return False
        old_category = product.category
        if old_category == new_category:
            return True

        # Remove from old category index
        if old_category in self.categories:
            self.categories[old_category].discard(sku)
            if not self.categories[old_category]:
                del self.categories[old_category]

        # Add to new category index
        if new_category not in self.categories:
            self.categories[new_category] = set()
        self.categories[new_category].add(sku)

        # Update product record
        product.category = new_category
        self.products[sku] = product

        # Invalidate category cache entries for old and new categories only
        self._category_cache.pop(old_category, None)
        self._category_cache.pop(new_category, None)

        return True

    def _invalidate_prefix_cache_for_name(self, name: str):
        """Invalidate only cache entries whose key is a prefix of `name`.

        For example, if name == 'Apple iPhone 13' then cached keys like
        'A', 'Ap', 'Apple ' will be invalidated. This keeps unrelated cached
        prefixes intact.
        """
        if not self._prefix_cache:
            return
        # Use the PrefixCacheTrie's O(m) invalidation (case-insensitive)
        self._prefix_cache.invalidate_prefixes_of_name(name)