# Saifuddings Savings Tracker
#প্রতি মাসে ৫০০০ টাকা জমায়
#লক্ষ্য: ৫০,০০০ টাকা জমানো
#প্রতি মাসে কত টাকা জমলো দেখাও
#এবং লক্ষ্য পূরণ হলে কত মাস লাগলো বলো

target=50000
monthly_saving=5000
month=1
total_saving=0

while total_saving<target :
    total_saving=monthly_saving+total_saving

    if total_saving==target:
        print("Month: ", month, "Total Saving Target Completed",total_saving)
    else:
        print("Month:",month,"Total Saving:",total_saving)
    
    month=month+1

