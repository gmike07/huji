from hangman import update_word_pattern
WORD_PLACE = 0
PATTERN_PLACE = 1
LETTER_PLACE = 2
CHECK_LIST = [["ddd", "___", "d"],
              ["dad", "___", "t"],
              ["aple", "__l_", "p"],
              ["spdppdpdddpd", "____________", "p"]]
#the first check tests if the function can access
# all indexes correctly (the first and last)
#the second check test if the function doesn't
# change the pattern when it shouldn't
#the third check test if the function changes only
# the correct index that meet the requirements
#the fourth check test if the function changes
# the correct indexes that meet the requirements when there is
# more than 1 and not everyone is the same letter

EXPECTED_LIST = ["ddd", "___", "_pl_", "_p_pp_p___p_"]
SUCCESS_MSG = 'Function "update_word_pattern" test success'
FAIL_MSG = 'Function "update_word_pattern" test fail'

def check_update_word_pattern():
    """
    the function checks if the function update_word_pattern works correctly,
    it prints if it works correctly or not
    and returns true if the function failed in a test it returns false,
                else true
    """
    success = True
    for i in range(len(CHECK_LIST)):
        updated_pattern = update_word_pattern(CHECK_LIST[i][WORD_PLACE],
                CHECK_LIST[i][PATTERN_PLACE], CHECK_LIST[i][LETTER_PLACE])
        if  updated_pattern != EXPECTED_LIST[i]:
            success = False
    if success == True:
        print(SUCCESS_MSG)
    else:
        print(FAIL_MSG)
    return success
if __name__ == "__main__":
    check_update_word_pattern()