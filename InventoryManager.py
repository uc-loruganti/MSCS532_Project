from Product import Product
from TrieNode import Trie


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
        # Simple prefix cache to speed repeated prefix queries; cleared on updates
        self._prefix_cache: dict[str, list[str]] = {}

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

        # Update search trie
        self.search_trie.insert(product.name, product.sku)
        # Invalidate prefix cache entries affected by this product's name
        self._invalidate_prefix_cache_for_name(product.name)

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

        # Remove from search trie
        self.search_trie.delete(prod.name, sku)
        # Invalidate prefix cache entries affected by this product's name
        self._invalidate_prefix_cache_for_name(prod.name)

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
            skus = self.categories[category]
            # Return generator for large categories; but keep compatibility by returning list
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
        # normalize prefix to keep cache keys stable
        key = prefix
        skus = None
        if key in self._prefix_cache:
            skus = list(self._prefix_cache[key])
        else:
            skus = list(self.search_trie.search(prefix))
            self._prefix_cache[key] = list(skus)

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
            self.search_trie.insert(p.name, p.sku)

        # reset cache
        self._prefix_cache.clear()

    def _invalidate_prefix_cache_for_name(self, name: str):
        """Invalidate only cache entries whose key is a prefix of `name`.

        For example, if name == 'Apple iPhone 13' then cached keys like
        'A', 'Ap', 'Apple ' will be invalidated. This keeps unrelated cached
        prefixes intact.
        """
        if not self._prefix_cache:
            return
        to_delete = [k for k in self._prefix_cache.keys() if name.startswith(k)]
        for k in to_delete:
            del self._prefix_cache[k]