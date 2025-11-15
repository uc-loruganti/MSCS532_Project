from InventoryManager import InventoryManager

# Point of Sale (POS) System
class POSSystem:
    # Initialize POS with an inventory manager instance injected
    def __init__(self, inventory_manager : InventoryManager):
        self.inventory_manager = inventory_manager
    
    # Process a sale transaction
    # This function should:
    # 1. Check if the product exists and has sufficient quantity
    # 2. Update the inventory accordingly
    # 3. Print the total price of the sale
    def process_sale(self, sku: str, quantity: int) -> bool:
        product = self.inventory_manager.get_product_by_sku(sku)
        if not product:
            print(f"Product with SKU {sku} not found.")
            return False
        
        if product.quantity < quantity:
            print(f"Insufficient stock for product {product.name}. Available: {product.quantity}, Requested: {quantity}")
            return False
        
        # Update inventory
        new_quantity = product.quantity - quantity
        self.inventory_manager.update_quantity(product, new_quantity)
        
        total_price = product.price * quantity
        print(f"Sale processed for {quantity} units of {product.name}. Total price: ${total_price:.2f}")
        return True
    
    # Process a return transaction
    # This function should:
    # 1. Check if the product exists
    # 2. Update the inventory accordingly
    # 3. Print the total refund amount
    def process_return(self, sku: str, quantity: int) -> bool:
        product = self.inventory_manager.get_product_by_sku(sku)
        if not product:
            print(f"Product with SKU {sku} not found. So, adding it to inventory.")
            return False
        
        # Update inventory
        new_quantity = product.quantity + quantity
        self.inventory_manager.update_quantity(product, new_quantity)
        
        total_refund = product.price * quantity
        print(f"Return processed for {quantity} units of {product.name}. Total refund: ${total_refund:.2f}")
        return True