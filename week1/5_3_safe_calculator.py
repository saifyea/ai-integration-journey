"""
নাম: safe_calculator
Input: a, operator, b

operator হতে পারে: "+", "-", "*", "/"

যদি "/" এবং b==0 → "Error: শূন্য দিয়ে ভাগ নয়!"
যদি ভুল operator → "Error: ভুল operator!"
যদি সংখ্যা না   → "Error: সংখ্যা দাও!"

safe_calculator(10, "+", 5)  → 15
safe_calculator(10, "/", 0)  → "Error: শূন্য দিয়ে ভাগ নয়!"
safe_calculator(10, "%", 5)  → "Error: ভুল operator!"
safe_calculator(10, "+", "a")→ "Error: সংখ্যা দাও!"
"""
#safe_calculator
def safe_calculator(a,o,b):
    try:
        if o=="+":
            return a+b
        elif o=="-":
            return a-b
        elif o=="/":
            if b==0:
                return "Error: শূন্য দিয়ে ভাগ নয়!"
            return a/b
        elif o=="*":
            return a*b
        else:
            return "Error: ভুল operator!"
    
    except TypeError:
       
            return "Error: সংখ্যা দাও!"
    
    except Exception as e:
        return f"Unknown error {e}"
    
print("1st one:->",safe_calculator(10, "+", 5))
print("second one:->",safe_calculator(10, "/", 0))
print("third one:->",safe_calculator(10, "%", 5) )
print("forth one:->",safe_calculator(10, "+", "a"))
print("fifth one:->",safe_calculator(10, "-", 5))
