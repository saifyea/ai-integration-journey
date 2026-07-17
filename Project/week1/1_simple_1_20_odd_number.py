# ১ থেকে ২০ পর্যন্ত শুধু জোড় সংখ্যা print করো (2, 4, 6, 8... 20)

i=1
for i in range(1, 21):
    if i%2==0:
        print(i, end='')
        if i < 20:
            print(',', end='')
#another way    
for i in range(1, 21):
    if i % 2 == 0:
        print(i, end='')

#another way
for i in range(2, 21, 2):   # range(start, end, step)
    print(i, end='')
