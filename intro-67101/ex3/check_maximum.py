from ex3 import maximum
#############################################################
# FILE : check_maximum.py
# WRITER : Mike Greenbaum , mikeg , 211747639
# EXERCISE : intro2cs1 ex3 2018-2019
# DESCRIPTION: check that the function maximum in ex3 works correctly
#############################################################
checks = [[], [1.1,1.2,1.5,1.7], [1,1.9,0.5,0], [-1, -2, -3.3], [-1, 0, 3.3]]
#checks[0] checks whether the function works with an empty list
#checks[1] checks if the function works correctly with decimal places
#checks[2] checks if the function works correctly with diffrent types of number
#checks[3] checks if the function works correctly with negative numbers
#checks[4] checks if the function works correctly with negative numbers, positive ones, and form diffrent types

expected = [None, 1.7, 1.9, -1, 3.3]
TEST_STRING = "Test"
TEST_SUCCESS = "OK"; TEST_FAIL = "FAIL"
def test():
    """
    the function runs maximum of ex3 and returns true if all the test were successful else false
    it print each test and if it failed or passed
    """
    success = True
    for i in range(len(checks)):
        if maximum(checks[i]) != expected[i]:
            success = False
            print(TEST_STRING, str(i), TEST_FAIL)
        else:
            print(TEST_STRING, str(i), TEST_SUCCESS)
    return success



if __name__ == '__main__':
    test()
