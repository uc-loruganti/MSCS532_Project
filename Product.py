# Product class definition for an e-commerce inventory management application
class Product: 
    sku: str 
    name: str 
    price: float 
    quantity: int 
    category: str
    def __init__(self, sku: str, name: str, price: float, quantity: int, category: str): 
        self.sku = sku 
        self.name = name 
        self.price = price 
        self.quantity = quantity 
        self.category = category