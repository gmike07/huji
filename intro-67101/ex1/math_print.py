#############################################################
# FILE : math_print.py
# WRITER : Mike Greenbaum , mikeg , 211747639
# EXERCISE : intro2cs1 ex1 2018-2019
# DESCRIPTION: A simple program that prints the needed calculation, like e, pi, etc.
#############################################################
import math
def golden_ratio():
    """this function prints the golden ratio to the screen"""
    print((1 + math.sqrt(5)) / 2.0)
def six_cubed():
    """this function prints 6*6*6 to the screen"""
    print(math.pow(6, 3))
def hypotenuse():
    """this function prints the hypotenuse of a right angle triangle with sides 3 and 5 to the screen"""
    print(math.hypot(3, 5))
def pi():
    """this function prints pi to the screen"""
    print(math.pi)
def e():
    """this function prints e to the screen"""
    print(math.e)
def triangular_area():
    """this function prints the area of all right angle with sides i
        when i is a integer from 1 to 10 (including 10)"""
    print((1 * 1) / 2.0, (2 * 2) / 2.0, (3 * 3) / 2.0, (4 * 4) / 2.0, (5 * 5) / 2.0,
          (6 * 6) / 2.0, (7 * 7) / 2.0, (8 * 8) / 2.0, (9 * 9) / 2.0, (10 * 10) / 2.0)
if __name__ == '__main__':
    golden_ratio()
    six_cubed()
    hypotenuse()
    pi()
    e()
    triangular_area()
