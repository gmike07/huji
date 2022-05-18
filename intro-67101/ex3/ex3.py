#############################################################
# FILE : ex3.py
# WRITER : Mike Greenbaum , mikeg , 211747639
# EXERCISE : intro2cs1 ex3 2018-2019
# DESCRIPTION: A file that contains a vast amount of utility functions to work with lists
#############################################################
def input_list():
    """
    the function gets input string from users and returns a list of all of them,
    ends to collect data from user when the input is ""
    :return: a list of all user string input data
    """
    lst = list()
    while True:
        input_string = input()
        if input_string == "":
            return lst
        lst.append(input_string)

def concat_list(str_list):
    """
    the function gets a list of strings and returns a string of all the strings connected with " " between them
    :param str_list: gets a list of strings
    :return: returns a string of all the strings connected with " " between them
    """
    string = ''
    for i in range(len(str_list)):
        string += str_list[i] + " "
    return string[:-1] # ignore the space in the end

def maximum(num_list):
    """
    the function gets a list of numbers and returns the max in the list
    :param num_list: gets a list of int \ floats
    :return: returns the max value of the list
    """
    if len(num_list) == 0:
        return None
    num_max = num_list[0]
    for number in num_list:
        if num_max < number:
            num_max = number
    return num_max

def cyclic(lst1, lst2):
    """
    the function gets 2 lists and returns true if the list is a cyclic of one another, else false
    :param lst1: gets a list
    :param lst2: gets a list
    :return: true if the list is a cyclic of one another, else false
    """
    #if the lists have diffrent lengths, return false
    if len(lst1) != len(lst2):
        return False
    lst = lst1.copy()
    #check if the lists are the same n + 1 times, each time cycle the first list by 1 and recheck
    for i in range(len(lst1) + 1):
        if lst == lst2:
            return True
        #moves the value of the list one to the right and the most right to the left
        #i.e. cycles the list by 1
        lst = lst[1:] + [lst[0]]
    return False


def seven_boom(n):
    """
    the function gets an int and returns a list of the number from 1 to n,
    if the number divides by 7 or contains the digit 7 change it to boom
    :param n: gets an int
    :return: returns a list of the number from 1 to n,
    if the number divides by 7 or contains the digit 7 change it to boom
    """
    lst = list()
    for i in range(1, n + 1):
        if i % 7 == 0 or '7' in str(i):
            lst.append("boom")
        else:
            lst.append(str(i))
    return lst


def histogram(n, num_list):
    """
    the function gets an int and a list and returns a list from 0 to n - 1,
    that in place i contains how much the number i appeared in num_list
    :param n: gets an int
    :param num_list: gets a list of numbers
    :return: a list from 0 to n - 1, that in place i contains how much the number i appeared in num_list
    """
    histogram = [0] * n
    for number in num_list:
        if 0 <= number < n:
            histogram[number] += 1
    return histogram


def prime_factors(n):
    """
    the function gets an int and returns a list of prime dividers and each divider in the list appears the number
    of times it divided n
    :param n: gets an int
    :return: a list of prime numbers that divide n every prime appears the number of times it divided n
    """
    if n < 2:
        return []
    prime_list = list()
    for i in range(2, n + 1):
        while n % i == 0:
            prime_list.append(i)
            n = n / i
    return prime_list


def cartesian(lst1, lst2):
    """
    the function get 2 lists and returns a cartesian multiplication of the lists as if they were groups
    :param lst1: gets a list
    :param lst2: gets a list
    :return:  returns a cartesian multiplication of the lists as if they were groups
    """
    if len(lst1) == 0 or len(lst2) == 0:
        return []
    lst = list()
    for i in range(len(lst1)):
        for j in range(len(lst2)):
            lst.append([lst1[i], lst2[j]])
    return lst


def pairs(num_list, n):
    """
    the function gets a number and a list sand returns  all combinations of 2 elements in the list such that their sum
    is n
    if x,y is returned and x,y appear once in the list, y,x won't be returned
    :param num_list: gets a list of ints
    :param n: gets an int
    :return: returns a list of all combinations of 2 elements in the list such that their sum is n
    """
    lst = list()
    for i in range(len(num_list)):
        for j in range(i + 1, len(num_list)):
            if num_list[i] + num_list[j] == n:
                lst.append([num_list[i], num_list[j]])
    return lst
