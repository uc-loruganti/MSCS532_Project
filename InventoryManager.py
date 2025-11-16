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

    # Function to remove a product from the inventory
    # This function updates all data structures accordingly
    # 1 : Remove from primary hash table
    # 2 : Remove from category index
    # 3 : Remove from search trie
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
            # O(n) lookup in primary hash table
            return [self.products[sku] for sku in skus]
        return []

    # Retrieve products by name prefix using the search trie
    # Time complexity : O(m) + O(n)
    # where m is length of the prefix and n is number of matching products
    # Space complexity : O(n) for the returned list
    def get_products_by_name_prefix(self, prefix: str) -> list[Product]: 
        # O(n) lookup in search trie
        skus = self.search_trie.search(prefix)
        return [self.products[sku] for sku in skus]

    # Get all categories in the inventory
    # Time complexity : O(1)
    # Space complexity : O(n) for the returned list
    def get_categories(self):
        return list(self.categories.keys())