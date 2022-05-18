import math
InputString = 'Insert coefficients a, b, and c: '
NoSolString = 'The equation has no solutions'
OneSolString = 'The equation has 1 solution:'
TwoSolString1 = 'The equation has 2 solutions:'
TwoSolString2 = 'and'

def quadratic_equation(a, b, c):
    """
    gets the coefficients of a*x^2 + b*x + c, and returns the root(s) of the parabula if exists
    :param a: gets an int or a float
    :param b: gets an int or a float
    :param c: gets an int or a float
    :return: returns the root(s) of the a*x^2 + b*x + c if exists
    """
    delta = (b*b) - (4*a*c) # delta = b^2-4ac
    twoA = a + a
    if delta < 0:
        return None, None
    elif delta == 0:
        # the output should be -b / 2a because the sqrt is zero
        return -b / twoA, None
    else: # delta > 0
        sqrtDelta = math.sqrt(delta) # sqrtDelta = sqrt(b^2-4ac)
        ans1 = (-b - sqrtDelta) / twoA # get the first root
        ans2 = (-b + sqrtDelta) / twoA # get the second root
        return ans1, ans2


def quadratic_equation_user_input():
    """
    the function gets input from user and outputs the solution for the quadratic equation if exists
    """
    Input = input(InputString)
    a, b, c = Input.split()
    ans1, ans2 = quadratic_equation(float(a), float(b), float(c))
    if ans1 == None and ans2 == None:
        #if there are no solutions ans1 = ans2 = None
        print(NoSolString)
    elif ans2 == None:
        # if there is one solution ans1 = sol and  ans2 = None
        print(OneSolString, ans1)
    else:
        # there are two solution, print both of them
        print(TwoSolString1, ans1, TwoSolString2, ans2)
