from largest_and_smallest import largest_and_smallest
min1 = 0; mid1 = 0.0; max1 = 0.0
min2 = 1; mid2 = 1.3; max2 = 1.9
min3 = 1; mid3 = 2; max3 = 5
min4 = 1; mid4 = 2.3; max4 = 3.9
min5 = -1; mid5 = 1.3; max5 = 100
SUCCESS = 'Function 4 test success'
FAIL = 'Function 4 test fail'
def test_largest_and_smallest():
    """
    calls largest and smallest function 5 times, and checking whether the result is the expected one
    if it is the expected result, if print that it ran successfully and returns true, else prints
    that it failed it the test and returns false
    """
    # check what returns when value are the same and part of them are floats
    check1 = (max1, min1) == largest_and_smallest(min1, mid1, max1)
    # check what returns when values are the same except the decimal value
    check2 = (max2, min2) == largest_and_smallest(min2, mid2, max2)
    # check what returns when values are not in the correct order
    check3 = (max3, min3) == largest_and_smallest(max3, mid3, min3)
    # check what returns when values are not in the correct order and different types (part int, part float)
    check4 = (max4, min4) == largest_and_smallest(min4, max4, mid4)
    # check what returns when values are from different types and part of them are negative and not in the correct order
    check5 = (max5, min5) == largest_and_smallest(mid5, min5, max5)
    #ran contains a boolean whether all the runs succeeded
    ran = check1 and check2 and check3 and check4 and check5
    if ran:
        print(SUCCESS)
    else:
        print(FAIL)
    return ran

if __name__ == "__main__":
    test_largest_and_smallest()