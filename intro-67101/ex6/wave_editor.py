from wave_helper import *
import math
import os.path


STRING_TO_USER_MAIN = "enter a number to do the next things: " \
                      "\n1. edit the wav file " \
                      "\n2. combine 2 wav files " \
                      "\n3. create a wav file " \
                      "\n4. exit the program" \
                      "\n"
STRING_USER_GET_FILE_EDIT = "enter a file to edit: "
STRING_USER_GET_FILE_OUTPUT = "enter a file to save in: "
STRING_USER_GET_EDIT_FUNCTION = "enter a number to do the next things: " \
                                "\n1. reverse the wav file " \
                                "\n2. speed up the wav file " \
                                "\n3. speed down the wav file  " \
                                "\n4. turn up the audio of the wav file " \
                                "\n5. turn down the audio of the wav file " \
                                "\n6. low pass filter of the wav file " \
                                "\n"
EDIT_FILE = "1"
COMBINE_FILES = "2"
COMPOSITE_FILE = "3"
EXIT_PROGRAM = "4"

SEP_DURATION = 125
DEFAULT_FRAME_RATE = 2000

FREQUENCY = {"A": 440, "B": 494, "C": 523, "D": 587,
             "E": 659, "F": 698, "G": 784, "Q": 0}
REVERSE_FILE = "1"
SPEED_UP = "2"
SPEED_DOWN = "3"
VOLUME_UP = "4"
VOLUME_DOWN = "5"
LOW_PASS_FILTER = "6"
WRONG_INPUT_FILE_EDIT = 'error: plz enter a valid wav file location'
ERROR_OUTPUT_FILE = 'error: plz enter a valid output location'
WRONG_INPUT_CHOOSE_EDIT = 'error: plz choose one' \
                          ' of the mentioned above options'
CHANGE_AUDIO = "2"
SAVE_AUDIO = "1"
STRING_TRANSITION_MENU = "enter a number to do the next things: " \
                        "\n1. save the wav file " \
                        "\n2. reedit the wav file " \
                        "\n"
STRING_ERROR_TRANSITION_MENU = 'error: plz enter a valid input'
MAX_VALUE = 32767
MIN_VALUE = -32768
SCALAR_VOLUME_UP = 1.2
SCALAR_VOLUME_DOWN = 1 / SCALAR_VOLUME_UP

STRING_USER_GET_COMPOSITION = "enter a composition file:"
ERROR_COMPOSITION_INPUT = "you entered a wrong file composition, try again!"
COMPOSITION_INPUTS = {"A", "B", "C", "D", "E", "F", "G", "Q"}

STRING_USER_GET_FILE_COMBINE = "enter 2 files to combine: "
WRONG_COMBINE_INPUT_TYPE = "you entered a wrong number of spaces, plz fix!"
WRONG_COMBINE_FILE_INPUT = "you entered a wrong file location!"
WRONG_COMBINE_LOAD_FILE = "failed to load file, try again"

WRONG_MAIN_INPUT = "you entered a wrong input, choose a number from 1 to 4"


def main_program():
    """
    the function gets input from the user and determines what to do with it,
    if the input is 4, the function ends
    """
    user_input = input(STRING_TO_USER_MAIN)
    while user_input != EXIT_PROGRAM:
        if user_input == EDIT_FILE:
            frame_rate, data = handle_editing_file()
            transition_menu(frame_rate, data)
        elif user_input == COMBINE_FILES:
            combine_files()
        elif user_input == COMPOSITE_FILE:
            composite()
        elif user_input != EXIT_PROGRAM:
            print(WRONG_MAIN_INPUT)
        user_input = input(STRING_TO_USER_MAIN)


def handle_editing_file(frame_rate=-1, data=None):
    """
    the function gets a file, gets input what to do with the file, and after
    all changes made to the file and returns the edited frame_rate and data
    :param frame_rate: gets the frame rate (int) to store; default value is -1
    :param data: gets the data (list of lists of 2 ints); default value is None
    :return: returns the edited frame_rate and data
    """
    if frame_rate == -1:
        frame_rate, audio_data = input_edit_file()
    else:
        frame_rate, audio_data = frame_rate, data
    keep_going = True
    while keep_going:
        saved_data = audio_data  # if the user messes up the commands
        user_choice = input(STRING_USER_GET_EDIT_FUNCTION)
        audio_data = handle_data(audio_data, user_choice)
        if audio_data is None:
            print(WRONG_INPUT_CHOOSE_EDIT)
            audio_data = saved_data
        else:  # the operation was fine
            keep_going = False
    return frame_rate, audio_data


def input_edit_file():
    """
    the function runs until the user gave correct input to the edit file
    to the program and outputs error if the input is incorrect
    :return: the frame rate and data of the correct input file
    """
    file_name = input(STRING_USER_GET_FILE_EDIT)
    file_data = load_wave(file_name)
    while file_data == -1:
        print(WRONG_INPUT_FILE_EDIT)
        file_name = input(STRING_USER_GET_FILE_EDIT)
        file_data = load_wave(file_name)
    frame_rate, audio_data = file_data
    return frame_rate, audio_data


def save_file(frame_rate, audio_data):
    """
    the function runs until the user gave correct output to the edit file
    to the program and outputs error if the input is incorrect
    :param frame_rate: gets the frame rate (int) to store
    :param audio_data: gets the data (list of lists of 2 ints)
    :return: saves the data anf frame rate in the output file
    """
    output_file_name = input(STRING_USER_GET_FILE_OUTPUT)
    while save_wave(frame_rate, audio_data, output_file_name) == -1:
        print(ERROR_OUTPUT_FILE)
        output_file_name = input(STRING_USER_GET_FILE_OUTPUT)


def handle_data(data, user_input):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :param user_input: gets a string from 1 - 6 to indicate the user input
    :return: returns the edited data according to the input
    """
    if user_input == REVERSE_FILE:
        return reverse_data(data)
    if user_input == SPEED_UP:
        return speed_up_data(data)
    if user_input == SPEED_DOWN:
        return speed_down_data(data)
    if user_input == VOLUME_UP:
        return volume_data(data, SCALAR_VOLUME_UP)
    if user_input == VOLUME_DOWN:
        return volume_data(data, SCALAR_VOLUME_DOWN)
    if user_input == LOW_PASS_FILTER:
        return low_pass_filter(data)


def reverse_data(data):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :return: returns the data reversed
    """
    return data[::-1]


def speed_up_data(data):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :return: returns the data only in places 0,2,4,6,8....
    """
    return data[::2]


def speed_down_data(data):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :return: returns the data when between every 2 elements in the data
        there will be the average
        for example: [[0,0],[2,2]] --> [[0,0],[1,1],[2,2]]
    """
    lst = [data[0]]
    for i in range(1, len(data)):
        lst.append(mid_value([data[i - 1], data[i]]))
        lst.append(data[i])
    return lst


def low_pass_filter(data):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :return: returns a new data when the
        new_data[i] = average(data[i], data[i-1], data[i+1])
    """
    lst = []
    for i in range(len(data)):
        if i == 0:
            lst.append(mid_value([data[i], data[i + 1]]))
        elif i == len(data) - 1:
            lst.append(mid_value([data[i], data[i - 1]]))
        else:
            lst.append(mid_value([data[i - 1], data[i], data[i + 1]]))
    return lst


def mid_value(lst):
    """
    :param lst: gets a list of lists that HAVE the same length
        and contain integers
    :return: list of the arithmetical average of the given lists of the list
    """
    new_list = []
    for j in range(len(lst[0])):
        new_list.append(int(sum_j_index_list(j, lst) / len(lst)))
    return new_list


def sum_j_index_list(j, lst):
    """
    :param j: gets an index (int) in lst[0] to check the sum at
    :param lst: gets the list of list of 2 integers to sum
    :return: returns the sum of col j in the list
    """
    sum_j_index = 0
    for i in range(len(lst)):
        sum_j_index += lst[i][j]
    return sum_j_index


def volume_data(data, volume):
    """
    :param data: gets a list of list of  2 int to change according to the input
    :param volume: a float to know how much to multiple the list by
    :return: returns the data when data[i] = data[i] * scalar,
        if it is in range MIN_VALUE, MAX_VALUE, else it will
        the the one closer to data[i] between the 2
    """
    lst = []
    for i in range(len(data)):
        lst.append(mul_values(data[i], volume))
    return lst


def mul_values(data, scalar):
    """
    :param data: gets a list of ints with 2 values
    :param scalar: gets a float to scale the data by
    :return: returns a list of the data when each
    """
    return [squash_between_min_max(int(x * scalar)) for x in data]


def squash_between_min_max(number):
    """
    :param number: gets an int
    :return: returns the int if MIN<=number<=MAX else returns the closer
        value between Max,Min to number
    """
    return min(MAX_VALUE, max(MIN_VALUE, number))


def composite_one_sound(letter, end):
    """
    :param letter: gets a letter to compose
    :param end: gets how much samples should be made of the letter
    :return: returns a list of lists of 2 int such that they contain
        the symphony of the given letter for the end given time
    """
    lst = []
    for i in range(end):
        one_over_samples = FREQUENCY[letter] / DEFAULT_FRAME_RATE
        theta = 2 * math.pi * i * one_over_samples
        value = int(MAX_VALUE * math.sin(theta))
        lst.append([value, value])
    return lst


def composite():
    """
    the function gets an input, processes the symphony, then call the function
    transition_menu()
    """
    file_data = get_composite_input()
    data = []
    for i in range(0, len(file_data), 2):
        data.extend(composite_one_sound(file_data[i],
                                        int(file_data[i + 1]) * SEP_DURATION))
    transition_menu(DEFAULT_FRAME_RATE, data)


def get_composite_input():
    """
    the function makes sure the user file of composition is valid and
        returns the file's text as a list separated by spaces
        (after it checked that the list is a symphony)
    :return:
    """
    file_path = input(STRING_USER_GET_COMPOSITION)
    user_data = read_file(file_path)
    while type(user_data) == bool or \
            not meets_composition_requirements(user_data):
        print(ERROR_COMPOSITION_INPUT)
        file_path = input(STRING_USER_GET_COMPOSITION)
        user_data = read_file(file_path)
    return user_data


def read_file(file_path):
    """
    :param file_path: gets a file path (string)
    :return: returns false if the file is invalid, else it returns the
        content within the file as a list
        (every element is a word in the text file)
    """
    if not os.path.isfile(file_path):
        return False
    with open(file_path, "r") as reader:
        lst = []
        for line in reader.readlines():
            lst.extend(line.strip().split())
        reader.close()
    return lst


def meets_composition_requirements(user_input):
    """
    :param user_input: gets a list of strings
    :return: true if the input is a composition, else false
    """
    if len(user_input) % 2 != 0:
        return False
    # if the strings are not a subset of the options
    # then it is not a valid input
    if not set(user_input[::2]) <= COMPOSITION_INPUTS:
        return False
    # return set(''.join(user_input[1::2]) <= set("0123456789")}
    for i in range(1, len(user_input), 2):
        if not is_number(user_input[i]):
            return False
    return True


def is_number(string):
    """
    :param string: gets a string
    :return: returns true if the string can be converted into int, else false
    """
    for letter in string:
        if not letter.isdigit():
            return False
    return True


def gcd(x, y):
    """
    :param x: gets an int
    :param y: gets an int
    :return: returns the gcd of the two inputs
    """
    x, y = max(x, y), min(x, y)
    while y > 0:
        x, y = y, x % y
    return x


def combine_files():
    """
    the function gets two inputs from the user, combines them
    and then call the function transition_menu()
    """
    frame_rate1, data1, frame_rate2, data2 = get_combined_files_data()
    frame_rate = min(frame_rate1, frame_rate2)
    gc = gcd(frame_rate1, frame_rate2)
    data = combine_data(data1, data2, int(frame_rate1 / gc),
                        int(frame_rate2 / gc))
    transition_menu(frame_rate, data)


def get_combined_files_data():
    """
    the function handles getting input from the user and outputs error
     if the input is incorrect
    :return: returns the frame rate and data of the first file,
    then the frame rate and data of the second file
    """
    file1_data = -1
    file2_data = -1
    while file1_data == -1 or file2_data == -1:
        file1, file2 = get_input_combine_files()
        file1_data = load_wave(file1)
        file2_data = load_wave(file2)
        if file1_data == -1 or file2_data == -1:
            print(WRONG_COMBINE_FILE_INPUT)
    frame_rate1, data1 = file1_data
    frame_rate2, data2 = file2_data
    return frame_rate1, data1, frame_rate2, data2


def get_input_combine_files():
    """
    the function gets input from user and checks the user's length input was
        two words
    :return: returns the correct input of the user (string)
    """
    user_input = input(STRING_USER_GET_FILE_COMBINE)
    splitted_input = user_input.split()
    while len(splitted_input) != 2:
        print(WRONG_COMBINE_INPUT_TYPE)
        user_input = input(STRING_USER_GET_FILE_COMBINE)
        splitted_input = user_input.split()
    return splitted_input


def combine_data(data1, data2, num1, num2):
    """
    :param data1: gets the data of the first file
    :param data2: gets the data of the second file
    :param num1: gets the frame_rate of the first file (after gcd) (int)
    :param num2: gets the frame_rate of the second file (after gcd) (int)
    :return: the combined data of the first and second data
    the function CHANGES data1 and data2
    """
    # if the second data should be the shorter one, switch them
    if num2 < num1:
        data1, data2 = data2, data1
        num1, num2 = num2, num1
    data = []
    while len(data1) > 0 and len(data2) > 0:
        #  work with num1 numbers of data1 and num2 numbers of data2
        #  the delete them
        data.extend(mid_values(data1[:num1], data2[:num2]))
        if len(data1) < num1:  # i f the data cut in the middle,
            #  add the missing part
            data.extend(data2[len(data1):num1])
        del data2[:num2]
        del data1[:num1]
    #  if one data ended and the second one didn't, add it to the data list
    if len(data1) != 0:
        data.extend(extend_longest_data(data1, num1, num2))
    if len(data2) != 0:
        data.extend(extend_longest_data(data2, num1, num2))
    return data


def extend_longest_data(data, num1, num2):
    """
    :param data: gets the data (list of lists of 2 ints)
    :param num1: gets the frame_rate of the first file (after gcd) (int)
    :param num2: gets the frame_rate of the second file (after gcd) (int)
    the program adding data up to num1 deletes data up to num2 and repeats and
    :return: returns the extended data
    """
    lst = []
    while len(data) > 0:
        lst.extend(data[:num1])
        del data[:num2]
    return lst


def mid_values(data1, data2):
    """
    :param data1: gets the data of the first file
    :param data2: gets the data of the second file
    :return: returns a new data when data[i] = average (data1[i], data2[i])
        there might be data ignored from data2
    """
    data = []
    for i in range(len(data1)):
        if i < len(data2):
            data.append(mid_value([data1[i], data2[i]]))
        else:
            data.extend(data1[i:])
            break
    return data


def transition_menu(frame_rate, data):
    """
    :param frame_rate: gets the frame rate (int) to store
    :param data: gets the data (list of lists of 2 ints)
    ask the user to choose one of 2 options:
    - save the data
    - change the data
    """
    user_input = CHANGE_AUDIO
    while user_input != SAVE_AUDIO:
        user_input = input(STRING_TRANSITION_MENU)
        if user_input == CHANGE_AUDIO:
            frame_rate, data = handle_editing_file(frame_rate, data)
        elif user_input != SAVE_AUDIO:
            print(STRING_ERROR_TRANSITION_MENU)
    save_file(frame_rate, data)


if __name__ == '__main__':
    main_program()
