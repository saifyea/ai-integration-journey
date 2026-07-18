#১ থেকে ৩০ পর্যন্ত সংখ্যা print করো
#কিন্তু:
 #   যদি ৩ দিয়ে ভাগ হয় → সংখ্যার বদলে "AI" লেখো
  #  যদি ৫ দিয়ে ভাগ হয় → সংখ্যার বদলে "Code" লেখো
 #   যদি দুটোই হয়       → "AI Code" লেখো

for i in range(1, 31):
    if i % 3 == 0 and i % 5 == 0:   # ✅ আগে দুটো একসাথে check করো
        print("AI Code", end=" ")
    elif i % 3 == 0:
        print("AI", end=" ")
    elif i % 5 == 0:
        print("Code", end=" ")
    else:
        print(i, end=" ")


#Function with multiple return values
def calculate_bmi(weight, height):
    bmi=weight / (height*height)
    bmi=round(bmi,2)
    if bmi<18.5:
        category= "Underweight"
    elif bmi<25:  
        category ="Normal "
    elif bmi<30:
        category= "Overweight"
    else:
        category ="Obesity"
    
    return bmi, category
    

bmi_value,bmi_category=calculate_bmi(70, 1.75)
print("Your BMI value:", bmi_value)
print("Your BMI category:", bmi_category)

