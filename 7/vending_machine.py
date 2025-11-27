class VendingMachine:
    def __init__(self, inventory):
        self.balance = 0
        self.inventory = inventory

    def insert_money(self, amount):
        if not isinstance(amount, int):
            return self.balance
        if amount < 0:
            return self.balance
        
        self.balance += amount
        return self.balance
    
    def get_balance(self):
        return self.balance

    def buy(self, item):
        if item not in self.inventory:
            return False
        price = self.inventory[item]
        if self.balance < price:
            return False
        self.balance -= price
        return True
    
    def refund(self):
        refunded_amount = self.balance
        self.balance = 0
        return refunded_amount
