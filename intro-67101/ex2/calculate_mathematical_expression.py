PLUS = "+"; MINUS = "-"; MUL = "*"; DIV = "/" # constants that contain the operations
Error0Div = 0 # contains the number that should throw an error for the '/' operation
def calculate_mathematical_expression(num1, num2, operation):
    """
    the function gets two numbers and an operation and returns operation(num1,num2) if possible
    :param num1: gets an int or a float
    :param num2: gets an int or a float
    :param operation:  gets a string of an operation, if doesn't meet the requirements, the function will return None
    :return: returns operation(num1,num2) if defined well else None
    """
    if operation == PLUS:
        return num1 + num2
    elif operation == MINUS:
        return num1 - num2
    elif operation == MUL:
        return num1 * num2
    elif operation == DIV:
        if num2 == Error0Div:
            return None
        return num1 / num2
    else:
        return None


def calculate_from_string(string):
    """
    gets a string and returns the calculation of the mathematical expression if possible
    :param string: gets a string to compute: the string should be num (space) operation (space) num
    :return: returns the calculation from string if possible else false
    """
    num1, operation, num2 = string.split()
    return calculate_mathematical_expression(float(num1), float(num2), operation)

