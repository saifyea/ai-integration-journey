    
# তোমার ৬ মাসের Learning Plan Tracker
# প্রতি মাসে ২ ঘন্টা করে শিখলে কত ঘন্টা হবে দেখাও

daily_hours = 2
days_in_month = 30

for month in range(1, 7):
    monthly_hours = daily_hours * days_in_month
    print("Month", month, "Total Learning:", monthly_hours, "hours") 

    if monthly_hours >= 60:
        print("On Track! 🔥")

