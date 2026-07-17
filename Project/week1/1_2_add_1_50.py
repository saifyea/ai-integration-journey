# ১ থেকে শুরু করে যোগ করতে থাকো
# যখন মোট যোগফল ৫০ পার হবে — থামো
# এবং কততম সংখ্যায় থামলে সেটা দেখাও

total = 0

for i in range (1,50,1):
  
    total += i
    if total > 50:
        print("Stop at number:", i)
        print("Total sum:", total)
        break
   



    
   
