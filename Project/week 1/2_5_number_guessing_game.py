"""একটা Number Guessing Game বানাও
    - Secret number = 7
    - User ৩ বার চেষ্টা করতে পারবে
    - প্রতিবার guess করবে (input নেবে)
    - সঠিক হলে "জিতেছো! 🎉"
    - ভুল হলে "বড়" বা "ছোট" hint দেবে
    - ৩ বার ভুল হলে "হেরেছো 😢 সংখ্যাটা ছিল 7"

Hint:
    guess = int(input("সংখ্যা বলো: "))
"""


secret_number=7
input_count=0
total_input=3

while input_count<total_input:
    guess=int(input("সংখ্যা বলো: "))
    input_count+=1

    if guess==secret_number:
           print("You win the game")
           break
    elif guess>secret_number:
        print("Your given number is bigber, try again")
    else:
        print("Your given number is smaller, try again")
        
    if input_count==total_input and guess!=secret_number:
         print("You failed to enter secret number, that was", secret_number)

