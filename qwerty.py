countNumbers = 0
count = 0

def estDelitel(number):
    for i in range(0, 9 + 1):
        if (number + i) % 7 == 0:
             return True
    return False
    

for i in range(10_000, 99_999 + 1):
    if estDelitel(i):
        count += 1
    
    countNumbers += 1

print(count)
print(countNumbers)