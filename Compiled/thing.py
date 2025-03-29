
'''
number = 5000

stepCounter = 0
while number != 1:
    if number % 2 == 0:
        number //= 2
    else:
        number = number * 3 + 1
    stepCounter += 1
    print(number, stepCounter)

print(stepCounter)
print("".join(list(reversed(bin(stepCounter)[2:]))))
    '''

import time
while 1:
    for y in range(10):
        for x in range(10):
            print("*", end="")
        print("\n",end="")
    time.sleep(0.1)

    for i in range(100 + 10):
        print(chr(8),end="")
    