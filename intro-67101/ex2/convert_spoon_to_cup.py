SpoonsPerCup = 16 # a constant that contains the ratio spoons for one cup
def convert_spoon_to_cup(spoons):
    """
    the function gets a number of spoons and determines how many cups (float) are required for the spoons
    :param spoons: gets an int that represents the number of spoons
    :return:  returns a float that represent how many cups are needed for the spoons amount
    """
    return spoons / SpoonsPerCup