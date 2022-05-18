def largest_and_smallest(num1, num2, num3):
    """
    the function gets 3 numbers and returns the max and min of them (max first)
    :param num1: the input should be an int or a float
    :param num2: the input should be an int or a float
    :param num3: the input should be an int or a float
    :return: returns a tuple containing (Max(a,b,c),Min(a,b,c))
    """
    # min(min(a,b),c)=min(a,b,c)
    Min = min2(min2(num1, num2), num3) # min(min(a,b),c)=min(a,b,c) therefore Min has the min value
    Max = max2(max2(num1, num2), num3) # max(max(a,b),c)=max(a,b,c) therefore Max has the max value
    return Max, Min


def min2(num1, num2):
    """
    the function gets 2 numbers and returns the min of them
    :param num1: the input should be an int or a float
    :param num2: the input should be an int or a float
    :return: returns the min of between num1 and num2
    """
    if num1 <= num2:
        return num1
    return num2


def max2(num1, num2):
    """
        the function gets 2 numbers and returns the max of them
        :param num1: the input should be an int or a float
        :param num2: the input should be an int or a float
        :return: returns the max of between num1 and num2
        """
    if num1 >= num2:
        return num1
    return num2