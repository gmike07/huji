def is_it_summer_yet(Temp, num1, num2, num3):
    """
    determines if it is summer yet by checking whether at least 2 nums are bigger than Temp
    :param Temp: gets an int or a float
    :param num1: gets an int or a float (temp day1)
    :param num2: gets an int or a float (temp day2)
    :param num3: gets an int or a float (temp day3)
    :return: if at least 2 nums are bigger than Temp
    """
    return (Temp < num1 and Temp < num2) or (Temp < num2 and Temp < num3) or (Temp < num1 and Temp < num3)