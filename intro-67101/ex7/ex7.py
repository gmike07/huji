DOT = '.'
STAR = '*'
RIGHT_PATH = "r"
UP_PATH = "u"
LEFT_PARENTHESES = '('
RIGHT_PARENTHESES = ')'


def print_to_n(n):
    """
    :param n: gets a positive integer
    prints the numbers from 1 to n (every number in a new line)
    """
    if n <= 0:
        return
    print_to_n(n - 1)
    print(n)


def print_reversed(n):
    """
    :param n: gets a positive integer
    prints the numbers from n to 1 (every number in a new line)
    """
    if n <= 0:
        return
    print(n)
    print_reversed(n - 1)


def is_prime(n):
    """
    :param n: gets an int
    :return: true if n is prime else false
    """
    if n <= 1:
        return False
    return has_divisor_smaller_than(n, n)


def has_divisor_smaller_than(n, i):
    """
    :param n: gets an int
    :param i: gets an int
    :return: returns true if for all 2 <= j < i, n % j != 0, else false
    """
    if i <= 2:
        return True
    if n % (i - 1) == 0:
        return False
    return has_divisor_smaller_than(n, i - 1)


def exp_n_x(n, x, i=0):
    """
    :param n: gets an int
    :param x: gets a float
    :param i: gets an index of which part to calc now,
    init to 0 if no input is given
    :return: e^x up to the n-th degree of the taylor's polynom (float)
    """
    if n < i:
        return 0
    return exp_n_x(n, x, i + 1) + ((x ** i) / factorial(i))


def factorial(n):
    """
    :param n: gets an int
    :return: returns n! (int)
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def play_hanoi(hanoi, n, src, dest, temp):
    """
    :param hanoi: gets the hanoi object
    :param n: gets the number of disks to move
    :param src: gets the src stick
    :param dest: gets the dest stick
    :param temp: gets the temp stick
    moves all disks from src to dest
    """
    if n < 1:
        return
    play_hanoi(hanoi, n - 1, src, temp, dest)  # move n - 1 to temp
    hanoi.move(src, dest)  # move the n-th one to dest
    play_hanoi(hanoi, n - 1, temp, dest, src)  # move n - 1 from temp to dest


def print_sequences(char_list, n):
    """
    :param char_list: gets a list of diffrent letter
    :param n: gets the length of the word that should be created
    prints all words that can be created of the char_list by n length
    """
    if n < 0:
        return
    lst = get_sequences(char_list, n)
    print_lst(lst)


def get_sequences(char_list, n):
    """
    :param char_list: gets a list of diffrent letter
    :param n: gets the length of the word that should be created
    :return: returns a list of all words that can be created
    of the char_list by n length
    """
    if n == 0:
        return [""]
    if n == 1:
        return char_list
    lst = get_sequences(char_list, n - 1)
    new_lst = []
    for i in range(len(char_list)):
        for j in range(len(lst)):
            new_lst.append(char_list[i] + lst[j])
    return new_lst


def print_no_repetition_sequences(char_list, n):
    """
    :param char_list: gets a list of diffrent letter
    :param n: gets the length of the word that should be created
    prints all words that can be created
    of the char_list when no letter appears twice by n length
    """
    if n < 0:
        return
    lst = get_no_repetition_sequences(char_list, n)
    print_lst(lst)


def print_lst(lst):
    """
    :param lst: gets a list
    prints the list
    it is with for loop because for len(lst) > 1000, it would crash for example
    get_sequences(char_list, 4) when len(char_list) >= 6
    """
    for element in lst:
        print(element)


def get_no_repetition_sequences(char_list, n):
    """
    :param char_list: gets a list of diffrent letter
    :param n: gets the length of the word that should be created
    :return: returns a list of all words that can be created
    of the char_list when no letter appears twice by n length
    """
    if n == 0:
        return [""]
    if n == 1:
        return char_list
    lst = get_no_repetition_sequences(char_list, n - 1)
    new_lst = []
    for i in range(len(char_list)):
        for j in range(len(lst)):
            if char_list[i] not in lst[j]:
                new_lst.append(char_list[i] + lst[j])
    return new_lst


def up_and_right(n, k):
    """
    :param n: gets an int
    :param k: gets an int
    prints all the ways to go from (0,0) to (n,k) when n is right and k is up
    """
    if n < 0 or k < 0:
        return
    if n == 0 and k == 0:
        print()
        return
    lst = get_lst_up_and_right(n, k)
    print_lst(lst)


def get_lst_up_and_right(n, k):
    """
    :param n: gets an int
    :param k: gets an int
    :return: returns a list of string of all the ways to go
        from (0,0) to (n,k) when n is right and k is up
    """
    if n == 1 and k == 0:
        return [RIGHT_PATH]
    if n == 0 and k == 1:
        return [UP_PATH]
    lst1 = []
    lst2 = []
    if n >= 1:
        lst1 = get_lst_up_and_right(n - 1, k)
        add_string_to_elements(lst1, RIGHT_PATH)
    if k >= 1:
        lst2 = get_lst_up_and_right(n, k - 1)
        add_string_to_elements(lst2, UP_PATH)
    lst = lst1
    lst.extend(lst2)
    return lst


def add_string_to_elements(lst, string, i=0):
    """
    :param lst: gets a list of strings
    :param string: gets a string to append to the list
    :param i: an index (int) to update (init at 0)
    changes lst[i] = string + lst[i] to all 0 <= i < len(lst)
    """
    if len(lst) <= i:
        return
    lst[i] = string + lst[i]
    add_string_to_elements(lst, string, i + 1)


def parentheses(n):
    """
    :param n: gets an int
    :return returns a lst of all string
    options of parentheses with n parentheses
    """
    if n < 0:
        return
    return append_parentheses(n, [])


def append_parentheses(n, lst, string=""):
    """
    :param n: gets an int
    :param lst: gets a list of strings
    :param string: gets the current string that the function works upon
    :return: returns all options of elements of of parentheses of all elements
    """
    if len(string) == 2 * n - 1:  # this is the last char of the string
        lst.append(string + RIGHT_PARENTHESES)
        return lst
    if string.count(LEFT_PARENTHESES) == string.count(RIGHT_PARENTHESES):
        # the string has the same number of left and right parenthesis
        return append_parentheses(n, lst, string + LEFT_PARENTHESES)
    if string.count(LEFT_PARENTHESES) < n:  # you can add more to the (
        append_parentheses(n, lst, string + LEFT_PARENTHESES)
    if string.count(RIGHT_PARENTHESES) < n:  # you can add more to the )
        append_parentheses(n, lst, string + RIGHT_PARENTHESES)
    return lst


def flood_fill(image, start):
    """
    :param image: gets a 2D list of strings containing '*' or '.'
    :param start: gets a tuple of (x,y) position
    changes the list at x,y to contain '*' and recursively opens each element
    to the 4 sides of it, if it contains '.' redoes the function
    ASSUMES: the 4 corners of the matrix contain '*'
    """
    x, y = start
    if image[x][y] == DOT:
        image[x][y] = STAR
        flood_fill(image, (x + 1, y))
        flood_fill(image, (x - 1, y))
        flood_fill(image, (x, y - 1))
        flood_fill(image, (x, y + 1))
