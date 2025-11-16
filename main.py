
from InventoryManager import InventoryManager
from Product import Product
from POSSystem import POSSystem

if __name__ == "__main__":
    print("MSCS532 Project: Product and Inventory Management System")
    inventory = InventoryManager()
    inventory.populate_sample_data()
    print("Inventory Manager initialized with sample data.")
    print( """
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
    """)

    print("-----------------------------------------------------")
    """
    Point of Sale (POS) System operations demo
    1. Process a sale transaction
    2. Process a return transaction
    """
    # Initialize POS system with the inventory manager
    pos_system = POSSystem(inventory)
    print("************** POS SYSTEM OPERATIONS **************")
    print("POS System initialized.")
    print("-------------------------------------")
    print("1. Process a sale transaction")
    
    # Process a sale transaction
    pos_system.process_sale("SKU001", 50)

    product_by_sku = inventory.get_product_by_sku("SKU001")
    print("Product quantity after sale:", product_by_sku.quantity if product_by_sku else "Not found")

    # Test duplicate sku addition
    # inventory.add_product(product)

    print("-------------------------------------")
    print("2. Process a return transaction")
    # process a return transaction
    pos_system.process_return("SKU001", 20)

    # retrieve a product by SKU
    product_by_sku = inventory.get_product_by_sku("SKU001")
    print("Product quantity after return:", product_by_sku.quantity if product_by_sku else "Not found")
    print("-------------------------------------")







    print("************** INVENTORY MANAGEMENT SYSTEM OPERATIONS **************")
    """
        Invertory Management System operations demo
        1. Add a product
        2. Remove a product
        3. Update a product
        4. Retrieve a product by SKU
        5. Get all categories in the inventory
        6. Search products by name prefix
        7. Get all products in a category
    """

    print("1. Add a new product")
    product = Product("SKU123", "Sample Product", 19.99, 100, "Electronics")
    inventory.add_product(product)
    print("Added product:", product.name)
    added_product = inventory.get_product_by_sku("SKU123")
    print("Retrieved added product:", added_product.name if added_product else "Not found")

    print("-------------------------------------")
    print("2. Remove a product")
    # remove a product
    inventory.remove_product(product)
    print("Removed product:", product.name)
    removed_product = inventory.get_product_by_sku("SKU123")
    print("Retrieved removed product:", removed_product.name if removed_product else "Not found")

    print("-------------------------------------")
    print("3. Update quantity of a product")
    # update quantity of a product
    inventory.update_quantity("SKU001", 75)
    print("Updated quantity of product with SKU001 to 75")
    print("-------------------------------------")

    print("4. Retrieve a product by SKU 'SKU002'")
    # retrieve a product by SKU
    product_by_sku = inventory.get_product_by_sku("SKU002")
    if product_by_sku:
        print("Retrieved product:", product_by_sku.name, "Quantity:", product_by_sku.quantity)
    else:
        print("Product not found.")

    print("-------------------------------------")
    print("5. Get all categories in the inventory")
    # get all categories in the inventory
    categories = inventory.get_categories()
    print("Categories in inventory:", categories)

    print("-------------------------------------")
    print("6. Search products by name prefix")
    """
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
    """
    # Search products by prefix
    prefix = "Apple"
    matching_products = inventory.get_products_by_name_prefix(prefix)
    # skus
    print(f"SKUs matching prefix '{prefix}':", [p.sku for p in matching_products])

    print("-------------------------------------")
    print("7. Get all products in a category : Electronics")
    # Get all products in a category
    category = "Electronics"
    products_in_category = inventory.get_products_by_category(category)
    print(f"Products in category '{category}':", [p.name for p in products_in_category])