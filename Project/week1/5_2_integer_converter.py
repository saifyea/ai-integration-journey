#problem 2
print("-"*35)
"""
একটা function বানাও:
নাম: convert_to_int
Input: value (যেকোনো কিছু)

value কে integer এ convert করো
যদি সম্ভব না হয় → "Error: সংখ্যা না!"

convert_to_int("42")   → 42
convert_to_int("abc")  → "Error: সংখ্যা না!"
convert_to_int("3.14") → "Error: সংখ্যা না!"
"""

def convert_to_int(number):
    try:
        return int(number)
    
    except ValueError:
         return f"Error: This is not number"

    except Exception as e:
       return f"Unknown Error: {e}"
    
print(convert_to_int("5"))
print(convert_to_int("abc")) 
print(convert_to_int("3.14"))
