# User এর কাছ থেকে দুটো সংখ্যা নাও
# ভাগ করো — error handle করো

try:
    a=int(input("enter 1st value:"))
    b=int(input("enter 2nd value:"))
    result=a/b
  
except ZeroDivisionError:
    print ("Unable to devide zero")
except ValueError:
    print("Please enter 1-9 only")

else:
     print("Output:",result)

#Assignment 2
"""
একটা function বানাও:
নাম: safe_divide
Input: a, b

যদি b == 0    → "Error: শূন্য দিয়ে ভাগ নয়!"
যদি সফল হয়  → result return করো
যদি অন্য error → "Unknown Error!"

safe_divide(10, 2)  → 5.0
safe_divide(10, 0)  → "Error: শূন্য দিয়ে ভাগ নয়!"
safe_divide(10, "a") → "Unknown Error!

"""

def catch_error(a,b):
    try:
        #a=int(input("enter 1st value:"))
        #b=int(input("enter 2nd value:"))
        result=a/b
    
    except ZeroDivisionError:
        return "Unable to devide zero"
    except Exception:
        return "Unknown Error"

    return result

print(catch_error(10, 2))    
print(catch_error(10, 0))   
print(catch_error(10, "a"))  


## Real AI API call এ এরকম error handle করতে হয়
def call_ai_api(prompt):
    try:
        # API call simulate করছি
        if prompt == "":
            raise ValueError("Prompt খালি হতে পারবে না!")
        
        response = f"AI Response: {prompt} সম্পর্কে উত্তর দিচ্ছি..."
        return response

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unknown Error: {e}"

print(call_ai_api("Python কী?"))
print(call_ai_api(""))


def call_api(promt):
    try:
        if promt=="":
            raise ValueError("Input should not be zero")
        response=f"AI Response: {promt} is..."
        return response
    except ValueError as e:
        return f"Error:{e}"
    except Exception as e:
        return f"Unknonwn error: {e}"

print(call_api("Python"))  
print(call_api(""))

