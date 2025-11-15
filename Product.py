# Product class definition for an e-commerce application
class Product: 
    sku: str 
    name: str 
    price: float 
    quantity: int 
    category: str
    def __init__(self, sku, name, price, quantity, category): 
        self.sku = sku 
        self.name = name 
        self.price = price 
        self.quantity = quantity 
        self.category = category