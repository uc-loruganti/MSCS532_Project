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


    # Function to add a new product to the inventory
    # This function updates all data structures accordingly
    # 1 : Add to primary hash table
    # 2 : Update category index
    # 3 : Update search trie
    def add_product(self, product: Product): 
        # Add product to primary hash table if not already present
        if product.sku in self.products:
            print(f"Product with SKU {product.sku} already exists.")
            return
        self.products[product.sku] = product

        # Update category index with the new sku
        if product.category not in self.categories:
            self.categories[product.category] = set()
        self.categories[product.category].add(product.sku)

        # Update search trie
        self.search_trie.insert(product.name, product.sku)

    def remove_product(self, product: Product): 
        # self.products.remove(product)

        # Remove from primary hash table
        if product.sku in self.products:
            del self.products[product.sku]

        # Remove from category index
        if product.category in self.categories:
            self.categories[product.category].discard(product.sku)
            if not self.categories[product.category]:
                del self.categories[product.category]

        # Remove from search trie
        self.search_trie.delete(product.name, product.sku)


    # Update quantity of a product and other data structures if needed
    def update_quantity(self, product: Product, quantity: int): 
        if(product.sku not in self.products):
            print(f"Product with SKU {product.sku} does not exist.")
            return
        
        if(quantity < 0):
            print("Quantity cannot be negative.")
            return
        
        product.quantity = quantity
        self.products[product.sku] = product
        
        
    # Retrieve a product by its SKU
    # Return None if not found
    def get_product_by_sku(self, sku : str): 
        return self.products.get(sku, None)

    # Retrieve products by category
    def get_products_by_category(self, category: str):
        if category in self.categories:
            skus = self.categories[category]
            return [self.products[sku] for sku in skus]
        return []

    # Retrieve products by name prefix using the search trie
    def get_products_by_name_prefix(self, prefix: str):
        skus = self.search_trie.search(prefix)
        return [self.products[sku] for sku in skus]

    # Get all categories in the inventory
    def get_categories(self):
        return list(self.categories.keys())