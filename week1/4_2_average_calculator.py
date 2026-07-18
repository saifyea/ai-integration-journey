"""
নাম: calculate_average
Input: numbers (একটা list)
কাজ: list এর সব সংখ্যার গড় বের করো

Hint:
    sum() → সব সংখ্যা যোগ করে
    len() → কতটা আছে
    average = sum / len

calculate_average([80, 90, 75, 85, 95]) → 85.0
"""
numbers=[80, 90, 75, 85, 95]
total=sum(numbers)
number_of_value=len(numbers)
average_value=total/number_of_value

print(total)
print(number_of_value)
print(average_value)

def average_calculator(number):
    total=sum(number)
    average=total/len(number)
    return average

result=average_calculator([80, 90, 75, 85, 95])
print(result)

print("==========================Output of another way==================================")
"""
নাম: student_report
Input: student (একটা Dictionary)

student = {
    "name": "Saifuddin",
    "math": 85,
    "english": 90,
    "science": 78
}

কাজ:
- তিনটা subject এর average বের করো
- average >= 80 → "Excellent! 🌟"
- average >= 60 → "Good! 👍"
- else          → "Need Improvement 📚"

Output:
Saifuddin এর average: 84.33
Result: Excellent! 🌟
"""
student={
    "name": "Saifuddin",
    "math": 85,
    "english": 90,
    "science": 78
}


def average_calculator(student):
    average=(student['math']+student["english"]+student['science'])/3
    if average>=80:
        result= "Excellent! 🌟"
    elif average>=60:
        result= "Good! 👍"
    else:
        result= "Need Improvement 📚"
    return average,result


avg,result=average_calculator(student)
print(student["name"],"average is:", round(avg,2))
print("Result:",result)