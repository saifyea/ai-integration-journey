#  নাম: ai_project_estimator
#Input: project_type, hours_needed

def ai_project_calculator(project_type, hours_need):
    if project_type=="chatbot":
        rate=50
    elif project_type=="automation":
        rate=40
    elif project_type=="rag":
        rate=60
    else:
        rate=30
    
    cost = hours_need * rate
    
    if cost > 2000:
        return f"Premium Project 🏆: ${cost}"
    elif cost > 1000:
        return f"Standard Project ✅: ${cost}"
    else:
        return f"Starter Project 🚀: ${cost}"


ai_projects = [("chatbot", 50), ("automation", 40), ("rag", 15), ("data_analysis", 25)]
for project_type, hours in ai_projects:
    cost = ai_project_calculator(project_type, hours)
    print(project_type,"->", cost)       

