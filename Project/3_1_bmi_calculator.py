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

