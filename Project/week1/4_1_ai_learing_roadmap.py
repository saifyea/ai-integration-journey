"""
একটা list বানাও তোমার ৫টা skill দিয়ে
তারপর:
- list এর length print করো
- প্রথম skill print করো
- শেষ skill print করো
- নতুন একটা skill যোগ করো
- সব skills loop দিয়ে print করো
"""
skills=["Python","AI Integration","SQL","Office Application", "HTML"]
print(len(skills))
last_value=len(skills)-1
print(skills[last_value])
skills.append("CSS")
for skill in skills:
    print(skill)
