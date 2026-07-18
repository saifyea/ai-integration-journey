"""
একটা Student class বানাও:

__init__: name, age, grade
methods:
    show_info() → সব তথ্য দেখাও
    is_passed() → grade >= 50 হলে "Passed ✅"
                  grade < 50 হলে "Failed ❌"
"""
class Student:
    def __init__(self,name,age,grade):
        self.name=name
        self.age=age
        self.grade=grade

    def show_info(self):
        print(f"Name of the Student:{self.name}")
        print(f"Age of the Student:{self.age}")
        print(f"Grade of the Student:{self.grade}")

    def is_passed(self):
        if self.grade>=50:
            return f"{self.name} your are passed"
        else:
            return f"{self.name} your are Failed"

s1=Student("Saifuddin",37,80)
s1.show_info()
print(s1.is_passed())
