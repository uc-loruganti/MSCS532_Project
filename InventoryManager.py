from MSCS532_Project import Product


class InventoryManager: 
    def __init__(self): 
        # 1. Primary Hash Table 
        self.products: dict[str, Product] = {} 
        # 2. Category Index. Dictionary mapping category to set of SKUs
        self.categories: dict[str, set[str]] = {} 

    
    def add_product(self, product): 
        # Add product to primary hash table
        self.products[product.sku] = product
        # Update category index
        if product.category not in self.categories:
            self.categories[product.category] = set()
        self.categories[product.category].add(product.sku)

    def remove_product(self, product): 
        self.products.remove(product)

    def update_quantity(self, product, quantity): 
        product.quantity = quantity 
    
    def get_product_by_sku(self, sku): 
        for product in self.products: 
            if product.sku == sku: 
                return product 
        return None