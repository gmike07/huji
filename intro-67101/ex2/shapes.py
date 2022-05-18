import math
InputString = 'Choose shape (1=circle, 2=rectangle, 3=triangle): '
TriangularAreaConst = math.sqrt(3) / 4 # contains sqrt(3) / 4 to calculate the area of a triangular
CircleChoice = 1 # contains the value of choosing circle
RectChoice = 2 # contains the value of choosing rectangle
TriaChoice = 3 # contains the value of choosing triangle

def shape_area():
    """
    awaits user input for a shape, and returns the area of that specific shape
    """
    Input = int(input(InputString))
    if Input == CircleChoice:
        return circle_area()
    elif Input == RectChoice:
        return rectangle_area()
    elif Input == TriaChoice:
        return triangle_area()

def circle_area():
    """
    awaits user input for a radius and returns the area of that circle
    :return: returns a float that contains the area of a circle with user's radius
    """
    r = float(input())
    return (r * r) * math.pi

def rectangle_area():
    """
    awaits for 2 user input for length of a rectangle and returns the area of that rectangle
    :return: returns a float that contains the area of a rectangle with user's inputs
    """
    width = float(input())
    height = float(input())
    return width * height

def triangle_area():
    """
    awaits for  user input for length of a triangle and returns the area of that triangle
    :return: returns a float that contains the area of a triangle with user's inputs
    """
    length = float(input())
    return (length * length) * TriangularAreaConst