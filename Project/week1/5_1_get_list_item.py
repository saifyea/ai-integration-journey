# Problem 1 — Easy
print("-"*35)
"""
একটা function বানাও:
নাম: get_list_item
Input: my_list, index

list থেকে index দিয়ে item বের করো
যদি index না থাকে → "Error: Index নেই!"
যদি অন্য error   → "Unknown Error!"

get_list_item([1,2,3], 1)  → 2
get_list_item([1,2,3], 10) → "Error: Index নেই!"
"""
def get_list_item(my_list,index):
    
    try:
        return my_list[index]
    
    except IndexError:
        return f"Error:Index not found"
    
    except Exception as e:
        return f"Unnkonwn Error {e}"
    


print(get_list_item([1,2,3], 2) )
print(get_list_item([1,2,3], 10))