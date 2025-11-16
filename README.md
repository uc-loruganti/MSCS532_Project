# MSCS532_Project

This project is a proof-of-concept implementation of an inventory management system for an e-commerce application. It utilizes several data structures to demonstrate core functionalities like product management, sales and returns processing, and efficient product searching.

## Core Data Structures

- **Hash Table (Python Dictionary):** The primary data structure for storing products, mapping a unique SKU to a `Product` object. This allows for O(1) average time complexity for insertions, deletions, and lookups.
- **Trie (Prefix Tree):** Implemented to enable efficient prefix-based searching of product names. This is crucial for features like auto-complete in a search bar.
- **Secondary Hash Table for Indexing:** A dictionary is used to index products by category, allowing for quick retrieval of all products belonging to a specific category.

## How to Run

To run the program and see a demonstration of its features, execute the following command in your terminal from the project's root directory:

```bash
python main.py
```

## Sample Output

```
MSCS532 Project: Product and Inventory Management System
Inventory Manager initialized with sample data.

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
    
-----------------------------------------------------
************** POS SYSTEM OPERATIONS **************
POS System initialized.
-------------------------------------
1. Process a sale transaction
Sale processed for 50 units of Apple iPhone 13. Total price: $39999.50
Product quantity after sale: 0
-------------------------------------
2. Process a return transaction
Return processed for 20 units of Apple iPhone 13. Total refund: $15999.80
Product quantity after return: 20
-------------------------------------
************** INVENTORY MANAGEMENT SYSTEM OPERATIONS **************
1. Add a new product
Added product: Sample Product
Retrieved added product: Sample Product
-------------------------------------
2. Remove a product
Removed product: Sample Product
Retrieved removed product: Not found
-------------------------------------
3. Update quantity of a product
Updated quantity of product with SKU001 to 75
-------------------------------------
4. Retrieve a product by SKU 'SKU002'
Retrieved product: Samsung Galaxy S21 Quantity: 30
-------------------------------------
5. Get all categories in the inventory
Categories in inventory: ['Electronics', 'Audio', 'Computers']
-------------------------------------
6. Search products by name prefix
SKUs matching prefix 'Apple': ['SKU005', 'SKU001']
-------------------------------------
7. Get all products in a category : Electronics
Products in category 'Electronics': ['Samsung Galaxy S21', 'Google Pixel 6', 'OnePlus 9 Pro', 'Apple iPhone 13']
```
