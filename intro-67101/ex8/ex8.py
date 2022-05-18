import math

NOT_FILLED = 0


def solve_sudoku(board):
    """
    :param board: gets a sudoku board
    :return: solves the board if possible, returns true if the board is solves,
    and updates the board to contain the solution, else returns false
    """
    numbers = list(range(1, len(board) + 1))
    solve_board(board, numbers)
    if board_solved(board):
        return True
    return False


def solve_board(board, numbers, x=0, y=0):
    """
    :param board: gets a sudoku board
    :param numbers: gets all options for choice in board
    :param x: gets an index in the board (int)
    :param y: gets an index in the board (int)
    tries to solve the board, updates if success else returns the board state
    that was before the call
    """
    if x >= len(board):
        return
    if y >= len(board):
        return solve_board(board, numbers, x + 1, 0)
    if board[x][y] != NOT_FILLED:
        return solve_board(board, numbers, x, y + 1)
    for option in numbers:
        handle_single_option(board, x, y, numbers, option)


def handle_single_option(board, x, y, numbers, option):
    """
    :param board: gets a sudoku board
    :param x: gets an index in the board (int)
    :param y: gets an index in the board (int)
    :param numbers: gets all options for choice in board
    :param option: gets the number that was chosen to try to continue with
    tries to solve the board after the option guess in x,y,
    updates if success else returns the board state that was before the call
    """
    if can_guess_option(board, x, y, option):
        board[x][y] = option
        solve_board(board, numbers, x, y + 1)
        if board_solved(board):
            return
        board[x][y] = NOT_FILLED


def can_guess_option(board, x, y, number):
    """
    :param board: gets a sudoku board
    :param x: gets an index in the board (int)
    :param y: gets an index in the board (int)
    :param number: gets all number to guess (int)
    :return: returns true if the number is not in the row, col and block,
    else false
    """
    return can_guess_row(board, x, number) \
           and can_guess_col(board, y, number) \
           and can_guess_block(board, x, y, number)


def can_guess_row(board, x, number):
    """
    :param board: gets a sudoku board
    :param x: gets an index in the board (int)
    :param number: gets all number to guess (int)
    :return: returns true if the number is not in the row, else false
        """
    for i in range(len(board)):
        if board[x][i] == number:
            return False
    return True


def can_guess_col(board, y, number):
    """
    :param board: gets a sudoku board
    :param y: gets an index in the board (int)
    :param number: gets all number to guess (int)
    :return: returns true if the number is not in the col, else false
    """
    for i in range(len(board)):
        if board[i][y] == number:
            return False
    return True


def can_guess_block(board, x, y, number):
    """
    :param board: gets a sudoku board
    :param x: gets an index in the board (int)
    :param y: gets an index in the board (int)
    :param number: gets all number to guess (int)
    :return: returns true if the number is not in the block, else false
    """
    length = int(math.sqrt(len(board)))
    x1 = x - x % length
    y1 = y - y % length
    for i in range(length):
        for j in range(length):
            new_x, new_y = x1 + i, y1 + j
            if not (x == new_x and y == new_y):
                if board[new_x][new_y] == number:
                    return False
    return True


def board_solved(board):
    """
    :param board: gets a sudoku board
    :return: returns true if the board has no tiles that are unfilled,
    else false
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == NOT_FILLED:
                return False
    return True


def print_k_subsets(n, k):
    """
    :param n: gets an int
    :param k: gets an int
    prints all subsets of {0,...n-1} of length k
    """
    if 0 <= k <= n:
        lst = [False] * n
        print_k_subsets_helper(lst, k)


def print_k_subsets_helper(lst, k, index=0, picked=0):
    """
    :param lst: gets a list of booleans that contain the choices up to now
    :param k: gets the length of the subset (int)
    :param index: gets the start index from where to start the subset
        (0 at first)
    :param picked: gets an int, at first 0, contains the amount of
        choices up to now
    prints all subsets of {0,...n-1} of length k
    """
    if k == picked:
        print_set(lst)
        return
    if index == len(lst):
        return
    lst[index] = True
    print_k_subsets_helper(lst, k, index + 1, picked + 1)
    lst[index] = False
    print_k_subsets_helper(lst, k, index + 1, picked)


def print_set(lst):
    """
    :param lst: gets a list of boolean true or false
    prints the list as int when i is in the list only if lst[i] = true
     """
    new_lst = []
    for i in range(len(lst)):
        if lst[i]:
            new_lst.append(i)
    print(new_lst)


def fill_k_subsets(n, k, lst):
    """
    :param n: gets an int
    :param k: gets an int
    :param lst: gets a lst to fill with all all subsets of {0,...n-1}
     of length k
    fills the lst with list of all subsets of {0,...n-1} of length k
    """
    if 0 <= k <= n:
        lst1 = [False] * n
        fill_k_subsets_helper(lst, lst1, k)


def fill_k_subsets_helper(lst, lst1, k, index=0, picked=0):
    """
    :param lst: gets a list of all correct lists up to now
    :param lst1: gets a list of booleans that contain the choices up to now
    :param k: gets the length of the subset (int)
    :param index: gets the start index from where to start the subset
        (0 at first)
    :param picked: gets an int, at first 0, contains the amount of
        choices up to now
    fills the lst with list of all subsets of {0,...n-1} of length k
    """
    if k == picked:
        lst.append(convert_set(lst1))
        return
    if index == len(lst1):
        return
    lst1[index] = True
    fill_k_subsets_helper(lst, lst1, k, index + 1, picked + 1)
    lst1[index] = False
    fill_k_subsets_helper(lst, lst1, k, index + 1, picked)


def convert_set(lst):
    """
    :param lst: gets a list of boolean true or false
    :return: the list as int when i is in the list only if lst[i] = true
     """
    new_lst = []
    for i in range(len(lst)):
        if lst[i]:
            new_lst.append(i)
    return new_lst


def return_k_subsets(n, k, index=0):
    """
    :param n: gets an int
    :param k: gets an int
    :param index: gets an index, at first should be 0
    :return: returns a list of all subsets of {0,...n-1} of length k
    """
    if k < 0:
        return []
    if k == 0:
        return [[]]
    if k == 1:
        return [[i] for i in range(index, n)]
    lst = []
    for i in range(index, n):
        lst1 = return_k_subsets(n, k - 1, i + 1)
        for element in lst1:
            lst.append([i] + element)
    return lst
