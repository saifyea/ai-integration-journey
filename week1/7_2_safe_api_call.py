
#🟡 Problem 4 — Medium (Error Handling + API)
print("-"*40,"output problem 4","-"*35)
"""
নাম: safe_api_call
Input: url

API call করো এবং error handle করো:
- status_code != 200 হলে → "Error: API কাজ করছে না!"
- Exception হলে → "Error: Internet সমস্যা!"
- সফল হলে → data return করো

এটা test করো ভুল URL দিয়ে:
safe_api_call("https://api.github.com")      ✅
safe_api_call("https://wrong-url-12345.com") ❌
"""

import requests

def safe_api_call(url):
    try:
       response=requests.get(url, timeout=5)

       if response.status_code!=200:
           raise ValueError(f"Error: API কাজ করছে না!")
       else:           
           return f"Status: {response.status_code}"
    
    except ValueError as e:
        return f"Error: {e}"
    except requests.exceptions.RequestException:
        return f"Error: Internet সমস্যা!"
    except Exception as e:
        return f"Unknown Error: {e}"

    

print(safe_api_call("https://api.github.com")  )  
print(safe_api_call("https://wrong-url-12345.com"))
