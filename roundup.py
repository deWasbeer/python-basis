# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def roundup(number):
    number=round(number,1)
    if number - round(number) > 0.5:
        number = round(number) + 1
    elif number - round(number) > 0.0:
        number = round(number) + 0.5
    else:
        number = round(number)
    return number

def main():
    x= 6.66
    y= 4.32
    z= 3.
    
    print(roundup(x))
    print(roundup(y))
    print(roundup(z))
    
main()