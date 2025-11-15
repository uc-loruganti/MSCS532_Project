from Product import Product
from TrieNode import TrieNode


# Inventory Manager class definition for managing products.
# Uses multiple data structures for efficient operations. 
# 1. Primary Hash Table for SKU to Product mapping.
# 2. Category Index for category-based retrieval.
# 3. Search Trie for fast name-based retrieval.
class InventoryManager: 
    def __init__(self): 
        # 1. Primary Hash Table 
        self.products: dict[str, Product] = {} 
        # 2. Category Index. Dictionary mapping category to set of SKUs
        self.categories: dict[str, set[str]] = {} 
        # 3. Search Trie 
        self.search_trie = TrieNode()



    def add_product(self, product: Product): 
        # Add product to primary hash table
        self.products[product.sku] = product

        # Update category index
        if product.category not in self.categories:
            self.categories[product.category] = set()
        self.categories[product.category].add(product.sku)

        # Update search trie
        self.search_trie.insert(product.name, product.sku)

    def remove_product(self, product: Product): 
        self.products.remove(product)

    def update_quantity(self, product: Product, quantity: int): 
        product.quantity = quantity 

    def get_product_by_sku(self, sku : str): 
        return self.products.get(sku, None)

    def get_products_by_category(self, category: str):
        if category in self.categories:
            skus = self.categories[category]
            return [self.products[sku] for sku in skus]
        return []

    def get_categories(self):
        return list(self.categories.keys())