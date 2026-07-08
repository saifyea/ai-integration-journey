# একটা Product class বানাও
class Product:
    def __init__(self, name,price, stock):
            self.name=name
            self.stock=stock
            self.price=price
        
    def show_info(self):
        print(f"Product name:{self.name}")
        print(f"Product Price:{self.price}")
        print(f"Product stock:{self.stock}")
    
    def is_available(self):
         if self.stock>0:
              return f"{self.name} is available"
         else:
            return f"{self.name} is not available"
    #qty add kora
    def sell(self,qty):
         if qty>self.stock:
              return f"Error: পর্যাপ্ত stock নেই!"
         self.stock=self.stock-qty
         return f"বিক্রি হয়েছে! বাকি stock: {self.stock}"

    def restock(self,qty):
        self.stock=self.stock+qty
        return f"Stock update হয়েছে! নতুন stock: {self.stock}"

# Object বানাও
p1=Product("Bangladesh Map",500,10)
p1.show_info()
print(p1.is_available())
print(p1.sell(1))
print(p1.sell(20))
print(p1.restock(3))


#একটা SimpleAI class বানাও:
class SimpleAI:
    def __init__(self,ai_name,model):
          self.ai_name=ai_name
          self.model=model
          self.total_queries=0

    def ask(self,question):
        self.total_queries=self.total_queries+1
        return f"AI Response: '{question}' সম্পর্কে উত্তর দিচ্ছি..."
    
    def show_stats(self):
        print(f"Name:{self.ai_name}")
        print(f"Model:{self.model}")
        print(f"Total Queries:{self.total_queries}")
    


ai = SimpleAI("Claude", "Sonnet")
print(ai.ask("Python কী?"))
print(ai.ask("AI কী?"))
ai.show_stats()



