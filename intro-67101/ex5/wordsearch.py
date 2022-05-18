import sys
import os.path

NUM_OF_INPUTS = 4 + 1
ERROR_WRONG_PARAMETER_NUMBER = 'error: wrong number of parameters,' \
                               ' expected 4 parameters!'
ERROR_WRONG_FILES_PATHS = 'error: wrong file path, file doesnt exist!'
ERROR_WRONG_DIRECTIONS = 'error: wrong direction is given!'
CREATE_WRITE_PARAMETER = 'w'
DIRECTIONS = ['u', 'd', 'r', 'l', 'w', 'x', 'y', 'z']
X_DIRECTIONS = {'u': 0, 'd': 0, 'r': 1, 'l': -1,
                'w': 1, 'x': -1, 'y': 1, 'z': -1}
Y_DIRECTIONS = {'u': -1, 'd': 1, 'r': 0, 'l': 0,
                'w': -1, 'x': -1, 'y': 1, 'z': 1}
READ_FILE = 'r'
SEPARATE_CHAR = ','
MINIMUM_INDEX = 0
NO_APPEARANCE = 0
INC_APPEARANCE = 1
WORD_FILE = 1
MAT_FILE = 2
OUT_FILE = 3
DIRS = 4
NEW_LINE = '\n'


def check_input_args(args):
    """
    :param args: a tuple containing 5 values:
    the first one is ignored (the name of this file)
    the second one should be a string containing a path to the word_list file
    the third one should be a string containing a path to the matrix file
    the fourth one should be a string containing a path to the output file
    the fifth one should be a string containing all directions to look at
    checks input and calls unctions to process the input if the input is valid
    if input is valid call process_files
    :return: if the inputs are correct it returns None, else returns the Error
    """
    if len(args) != NUM_OF_INPUTS:
        return ERROR_WRONG_PARAMETER_NUMBER
    s, words_file_path, matrix_file_path, output_file_path, directions = args
    return handle_wrong_inputs(words_file_path, matrix_file_path, directions)


def process_files(words_file_path, matrix_file_path, output_file_path,
                  directions):
    """
    :param words_file_path:gets a string containing
                a path to the word_list file
    :param matrix_file_path: gets a string containing
                a path to the matrix file
    :param output_file_path: gets a string containing
                a path to the output file
    :param directions: gets a string containing all directions to look at
    the functions call the function to read the files and to output the results
    """
    word_list = read_wordlist_file(words_file_path)
    matrix = read_matrix_file(matrix_file_path)
    results = find_words_in_matrix(word_list, matrix, directions)
    write_output_file(results, output_file_path)


def write_output_file(results, output_file_path):
    """
    :param results: gets a list of tuples of results when the keys
        are string that appear more then once and the values are integers
    :param output_file_path: a path to the file to write the results in

    the function outputs the results to the output file, in the next format:
        key, value + \n
    closes the file after usage
    """
    output = ''
    with open(output_file_path, CREATE_WRITE_PARAMETER) as output_file:
        for key, value in results:
            output += (key + SEPARATE_CHAR + str(value)) + NEW_LINE
        # delete \n in the last line
        output_file.write(output[:-len(NEW_LINE)])
        output_file.close()


def handle_wrong_inputs(words_file_path, matrix_file_path, directions):
    """
    :param words_file_path:gets a string containing
                a path to the word_list file
    :param matrix_file_path: gets a string containing
                a path to the matrix file
    :param directions: gets a string containing all directions to look at
    :return: returns why aren't they valid if the aren't valid, else None
    """
    if file_doesnt_exists(words_file_path) or \
            file_doesnt_exists(matrix_file_path):
        return ERROR_WRONG_FILES_PATHS
    if not correct_direction_input(directions):
        return ERROR_WRONG_DIRECTIONS
    return None


def file_doesnt_exists(file_path):
    """
    :param file_path: gets a string
    :return: returns true if it is NOT a file, else false
    """
    return not os.path.isfile(file_path)


def correct_direction_input(directions):
    """
    :param directions: gets a string containing all directions to look at
    :return: returns true if all directions are valid, else false
    """
    for direction in directions:
        if direction not in DIRECTIONS:
            return False
    return True


def read_wordlist_file(filename):
    """
    :param filename: gets a string containing a path to a file
    :return: returns a list of all words in the file
            (Every word is in a new line in the file)
            closes the file after usage
    """
    with open(filename, READ_FILE) as reader_file:
        word_list = []
        for word in reader_file.readlines():
            word_list.append(word.strip())
        reader_file.close()
    return word_list


def read_matrix_file(filename):
    """
    :param filename: gets a string containing a path to a file
    :return: returns a matrix of all letters in the file
            (Every letter is separated by ,)
            closes the file after usage
    """
    matrix = []
    with open(filename, READ_FILE) as reader_file:
        for line in reader_file.readlines():
            matrix.append(line.strip().split(SEPARATE_CHAR))
        reader_file.close()
    return matrix


def find_words_in_matrix(word_list, matrix, directions):
    """
    :param word_list: gets a list of words to look for
    :param matrix: gets a 2D list of letter to search in
    :param directions: get all directions to look at
    :return: returns a list of tuples when the first value is a word that
        appear in the matrix in the given directions
        and the second value is  how many times the word appeared
    """
    words_in_matrix = {}
    for direction in set(directions):  # delete copies of letter that exist
        direction_dict = find_words_in_direction(word_list, matrix, direction)
        update_dictionary(words_in_matrix, direction_dict)
    return convert_dictionary_to_list(words_in_matrix)


def convert_dictionary_to_list(dictionary):
    """
    :param dictionary: gets a dictionary
    :return: returns the dictionary as a list of tuples of type:
        (key, value)
    """
    lst = []
    for key in dictionary:
        lst.append((key, dictionary[key]))
    return lst


def update_dictionary(dict1, dict2):
    """
    :param dict1: gets a dictionary with the second type of int
    :param dict2: gets a dictionary with the second type of int
    :return: updates the first dictionary
    if the key is already in dict1 then dict1 += dict2
    else dict1 = dict2 for that specific key
    """
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]


def find_words_in_direction(word_list, matrix, direction):
    """
    :param word_list: gets a list of words to look for
    :param matrix: gets a 2D list of letter to search in
    :param direction: get a direction to look at
    :return: all words that appear in the direction in
        the matrix in a dictionary with how many
        times they appeared as a dictionary
    """
    words_in_direction = {}
    for word in word_list:
        word_appearance = num_matrix_contains_word(word, matrix,
                                                   X_DIRECTIONS[direction],
                                                   Y_DIRECTIONS[direction])
        if word_appearance > NO_APPEARANCE:
            words_in_direction[word] = word_appearance
    return words_in_direction


def num_matrix_contains_word(word, matrix, x_dir, y_dir):
    """
    :param word: gets a word to check
    :param matrix: gets a 2D list of letter to search in
    :param x_dir: gets where to move in the x direction (int)
    :param y_dir: gets where to move in the y direction (int)
    :return: returns how many times the word
            appears in this direction in the matrix
    """
    word_appearance = NO_APPEARANCE
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix_contains_word_in_xy(word, matrix, x, y, x_dir, y_dir):
                word_appearance += INC_APPEARANCE
    return word_appearance


def matrix_contains_word_in_xy(word, matrix, x, y, x_dir, y_dir):
    """
    :param word: gets a word to check
    :param matrix: gets a 2D list of letter to search in
    :param x: gets a x index in the matrix (int)
    :param y: gets a y index in the matrix (int)
    :param x_dir: gets where to move in the x direction (int)
    :param y_dir: gets where to move in the y direction (int)
    :return: if the word is in the matrix
        from x,y to x + x_dir(n - 1), y + y_dir(n-1) when n = len(word)
    """
    x_last_place = x + x_dir * (len(word) - 1)
    y_last_place = y + y_dir * (len(word) - 1)
    #  if the last part of the word is not in the matrix at all,
    #  doesn't fit then return false
    if is_out_of_bounds(y_last_place, len(matrix)) or \
            is_out_of_bounds(x_last_place, len(matrix[y])):
        return False
    for i in range(len(word)):
        if word[i] != matrix[y][x]:  # check if each letter fits
            return False
        # update the x,y according to the dir that the function was given
        x += x_dir
        y += y_dir
    return True


def is_out_of_bounds(index, max_index):
    """
    :param index: gets an index in the list (int)
    :param max_index: gets the maximum index in the list (int)
    :return: returns true if the index is less than
            the minimum or greater or equal to the maximum
            i.e. true if list[index] will be an error
    """
    return index < MINIMUM_INDEX or index >= max_index


def main_program():
    """
    the function prints the error in the inputs if such exists,
     else processes the file
    """
    error = check_input_args(sys.argv)
    if error is None:
        process_files(sys.argv[WORD_FILE], sys.argv[MAT_FILE],
                      sys.argv[OUT_FILE], sys.argv[DIRS])
    else:
        print(error)


if __name__ == "__main__":
    main_program()
