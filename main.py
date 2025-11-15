
from InventoryManager import InventoryManager
from Product import Product

if __name__ == "__main__":
    print("MSCS532 Project: Product and Inventory Management System")
    inventory = InventoryManager()
    print("Inventory Manager initialized.")

    # Demo usage
    # add a sample product to the inventory
    product = Product("SKU123", "Sample Product", 19.99, 100, "Electronics")
    inventory.add_product(product)

    product_by_sku = inventory.get_product_by_sku("SKU1234")
    print("Retrieved product by SKU:", product_by_sku.name if product_by_sku else "Not found")

    categories = inventory.get_categories()
    print("Categories in inventory:", categories)