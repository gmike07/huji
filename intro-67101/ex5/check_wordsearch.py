from wordsearch import num_matrix_contains_word

WORD_PLACE = 0
MATRIX_PLACE = 1
X_DIR_PLACE = 2
Y_DIR_PLACE = 3
CHECK_LIST = [["", [[]], 1, 0],
              ["d", [[]], 1, 0],
              ["d", [[]], 0, 1],
              ["dad", [['d', 'a', 'd']], 1, 0],
              ["dad", [['d'], ['a'], ['d'], ['a'], ['d']], 0, 1]]
#  the first check tests if the function can work correctly for empty matrix

#  the second check test if the function works correctly for a string
#     longer than the matrix in the X direction

#  the third check test if the function works correctly for a string
#     longer than the matrix in the Y direction

#  the fourth check test if the function works correctly for finding a string
#       in the x dir string

#  the fifth check test if the function works correctly for finding multiple
#       strings in the y dir string


EXPECTED_LIST = [0, 0, 0, 1, 2]
SUCCESS_MSG = 'Function "num_matrix_contains_word" test success'
FAIL_MSG = 'Function "num_matrix_contains_word" test fail'


def check_num_matrix_contains_word():
    """
    the function checks if the function num_matrix_contains_word
       works correctly, it prints if it works correctly or not
       and returns true if the function failed in a test it returns false,
                   else true
       """
    success = True
    for i in range(len(CHECK_LIST)):
        word_appearance = num_matrix_contains_word(CHECK_LIST[i][WORD_PLACE],
                                                   CHECK_LIST[i][MATRIX_PLACE],
                                                   CHECK_LIST[i][X_DIR_PLACE],
                                                   CHECK_LIST[i][Y_DIR_PLACE])
        if word_appearance != EXPECTED_LIST[i]:
            success = False

    if success:
        print(SUCCESS_MSG)
    else:
        print(FAIL_MSG)
    return success


if __name__ == "__main__":
    check_num_matrix_contains_word()
