"""
def function_name(parameter):
    # কাজ করো
    return result

def     : to make funtion 
greet   : it is the name of the function
(name)  : it is the parameter of the function


"""
# Simple Function

from cmath import cos

def greet(name):
    print("Hello,", name, "! AI Journey Runnin 🚀")

greet("Saifuddin")
greet("Python")

# Function with return value
def calculate_hours(daily_hours, months):
    total = daily_hours * 30 * months
    return total

result = calculate_hours(2, 6)
print("Total in 6 months:", result, "hours")


# Function with conditional statements


def check_progress(hours):
    if hours>=100:
        return "Expart Level! 💪"
    elif hours>=50:
        return "Good Progress! 💪"
    else:
        return "Keep Learning! 📚"

result = check_progress(75)
print("Your progress:", result)





#function with conditional statements, loop and return value
def ai_salary_estimator(months):
    if months>=12:
        salary="Senior: $3000+/month"
    elif months>=6:
        salary="Mid: $1000-3000/month"
    elif months>=3:
        salary="Junior: $500-1000/month"
    else:
        salary='Fresher: $300-500/month'
    
    return months, salary   

for m in [15,2,8,6]:
    ai_months, ai_salary=ai_salary_estimator(m)
    print("AI Experience:", ai_months, "months and Salary", ai_salary)





#even odd number checker function
def is_odd_or_even (number):
    if number % 2 == 0:
        return  number, "is Even"
    else:
        return number, "is Odd"
    
for num in [10, 15, 22, 33]:
    num, result = is_odd_or_even(num)
    print (num, result)


#grade calculator function
def grade_calculator(score):
    if score>=90:
        return score, "A"
    elif score>=80:
        return score, "B"
    elif score>=70:
        return score, "C"
    elif score>=60:
        return score, "D"
    else:
        return score, "F"
    

for score in [95,49,75,80,60]:
    score, grade = grade_calculator(score)
    print("Score:",score, "Grade:", grade) 


#freelance income calculator function
def freelance_income(hourse_worked, rate_per_hour):
    income=hourse_worked * rate_per_hour
    return income

for hours,rate in [(10, 50), (20, 60), (5, 30)]:
    income = freelance_income(hours, rate)
    
    if income >= 1000:
        print("Great Week! 💰 $", income)
    elif income >= 500:
        print("Good Week! 💰 $", income)
    else:
        print("Keep Going! 💪 $", income)


