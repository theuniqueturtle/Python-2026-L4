# %% Ex1
def Ex1():
    x= float(input("Enter circle radius: "))
    circlearea= (x**2)*3.14
    print(f"circle area = {circlearea}")
Ex1()
# %% Ex2
def Ex2():
    celcius= float(input("Enter the temperature in celcius: "))
    F= (celcius*1.8)+32
    print(f"In Fahrenheit: {F}")
Ex2()

#%% Ex3
def Ex3():
    x= int(input("Enter a number: "))
    if x<2:
        print(f"{x} is not prime")
    else:
        y=0
        for i in range(2, x):
            if x%i==0:
                y=1
            break
        if y==1:
            print(f"{x} is not prime")
        else:
            print(f"{x} is prime")
Ex3()
# %% Ex4
def Ex4():    
    x= int(input("Enter your number: "))
    y=0
    for i in range(1, x):   
        if x % i == 0:
            y += i
    if y == x:
        print(f"{x} is a perfect number")
    else:
        print(f"{x} is not a perfect number")
Ex4()
# %% Ex5
def Ex5():    
    color = ["red", "blue", "green", "pink", "yellow"]
    x = input("Your fav color: ").lower()

    if x in color:
        x = color.index(x)
        print("your color found in the index")
    else:
        print("your color not found in the index")
Ex5()
# %% Ex6
def Ex6():
    x=0
    for i in range(0, 6):
        print(i, end=" ")
    print( )
    for i in range(1, 11, 3):
        print(i, end=" ")
    print( )
    for i in range(5, 0, -1):
        print(i, end=" ")
    print( )
    for i in range(6, -3, -2):
        print(i, end=" ")
    print( )
Ex6()
# %% Ex7
def remove_dollar_sign(s):
    new_string = s.replace("$", "")
    return new_string

s = str(input("Enter your number"))
print(s)
print(remove_dollar_sign(s))
# %% Ex8
def extract_even(l):
    result = []

    for x in l:
        if x % 2 == 0:
            result.append(x)

    return result

l = [1, 4, 5, -1, 10]
print("Input list:", l)
print("Even numbers:", extract_even(l))
# %% Ex9
def factorial(n):
    result = 1

    for i in range(1, n + 1):
        result = result * i

    return result
n = int(input("Enter a non-negative integer: "))
print(f"{n}! = {factorial(n)}")
# %% Ex10
def get_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

# %% Ex11
import math
def distance(x1, y1, x2, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d
x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))
x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))
print(f"Distance = {distance(x1, y1, x2, y2)}")

# %% Ex12
def print_pattern(m, n):
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print() 
print_pattern(m=5, n=7)
