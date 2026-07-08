# List বানানো
fruits=["apple", "banana", "orange"]
marks=[85, 90, 78]
value=[1, 2, 3, 4, "Mango", 5.5]


print(len(value))
for fruit in fruits:
    print(fruit)


# তোমার AI learning roadmap বানাও
roadmap=["Python", "API Basics", "Prompt Engineering",
           "LangChain", "RAG", "AI Agents"]

roadmap.append("test")
roadmap.remove('test')
for i,skill in enumerate(roadmap):
    print(i+1,"->", skill)

# Dictionary বানানো
profile = {
    "name": "Saifuddin",
    "experience": "12 years",
    "current_role": "Payroll & IT Manager",
    "goal": "AI Integration Specialist",
    "daily_hours": 2
}

for key,value in profile.items():
    print(key,"->",value)


projects={
   "project1":500,
   "project2":1500,
   "project3":1000
}

max_cost=0
max_project=""

for key,value in projects.items():
    if value>max_cost:
        max_cost=value
        max_project=key
    
print(max_project,"->",max_cost)

    
