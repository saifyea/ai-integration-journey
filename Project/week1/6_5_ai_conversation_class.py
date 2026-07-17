"""
একটা AIConversation class বানাও:

__init__: ai_name, history=[]
methods:
    chat(user_message)
        → history তে message যোগ করো
        → response তৈরি করো
        → history তে response যোগ করো
        → response return করো
    
    show_history()
        → সব conversation দেখাও
    
    clear_history()
        → history খালি করো
    
    total_messages()
        → মোট কতটা message হয়েছে

ai = AIConversation("Claude")
ai.chat("Python কী?")
ai.chat("AI কী?")
ai.show_history()
print(ai.total_messages())
"""
class AIConversation:
    def __init__(self,ai_name):
        self.ai_name=ai_name
        self.history=[]
        self.total_msg=0

    def show_history(self):
        for msg in self.history: 
             print(msg["role"], "→", msg["message"])
    
    def chat(self, user_msg):
        try: 
            if user_msg == "":
                raise ValueError("Message খালি!")
        
            self.history.append({
                "role":"user",
                "message":user_msg
            })
            response = f"AI: '{user_msg}' সম্পর্কে উত্তর দিচ্ছি..."
            self.history.append({
                "role":"Ai",
                "message":response
            })
            return response
        
        except ValueError as e:
            return f"Validation Error: {e}"
        except Exception as e:
            return f"API Error: {e}"   
    
    def  clear_history(self):
       self.history.clear()
       print("History cleared! ✅")
    
    def total_messages(self):
         return f"Total Messages: {len(self.history)}"

        #→ মোট কতটা message হয়েছে
   
    
ai = AIConversation("Claude")
ai.chat("Python কী?")
ai.chat("AI কী?")
ai.show_history()
print(ai.total_messages())