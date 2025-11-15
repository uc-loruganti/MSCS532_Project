
from InventoryManager import InventoryManager
from Product import Product
from POSSystem import POSSystem

if __name__ == "__main__":
    print("MSCS532 Project: Product and Inventory Management System")
    inventory = InventoryManager()
    inventory.populate_sample_data()
    print("Inventory Manager initialized with sample data.")
    
    # Initialize POS system with the inventory manager
    pos_system = POSSystem(inventory)
    print("POS System initialized.")




    # Demo usage
    # add a sample product to the inventory
    product = Product("SKU123", "Sample Product", 19.99, 100, "Electronics")
    inventory.add_product(product)
    print("Added product:", product.name)

    
    # Test duplicate sku addition
    # inventory.add_product(product)

    product_by_sku = inventory.get_product_by_sku("SKU123")
    print("Retrieved product by SKU:", product_by_sku.name if product_by_sku else "Not found")

    categories = inventory.get_categories()
    print("Categories in inventory:", categories)