"""
একটা BankAccount class বানাও:
__init__: owner, balance=0
methods:
    deposit(amount)  → balance বাড়াও
    withdraw(amount) → balance কমাও
                       যদি amount > balance → "Error: টাকা নেই!"
    show_balance()   → বর্তমান balance দেখাও

account = BankAccount("Saifuddin", 1000)
account.deposit(500)
account.withdraw(200)
account.withdraw(5000)
account.show_balance()
"""
print("-"*35)
class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.balance=balance
  
    def deposit(self,new_amount):
        self.balance+=new_amount
        print(f"New Deposit Amount:{self.balance}")
    
    def withdraw(self,w_amount):
        if self.balance<w_amount:
            print(f"{w_amount} this amount of fund is not available")
        else:
            self.balance-=w_amount
            print(f"New withdraw Amount:{self.balance}")    

    def show_balance(self):
        print(f"Account Holder:{self.owner}")
        print(f"Account Number:{self.balance}")



account=BankAccount("Saifuddin",5000)
account.deposit(500)
account.withdraw(20000)
account.withdraw(5000)
account.show_balance()
