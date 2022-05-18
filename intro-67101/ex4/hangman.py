from hangman_helper import *
ORD_A = ord('a')
IGNORE_NUM = -1
RESET_NUM = 0
INC_NUM = 1
HIDDEN_LETTER = '_'
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def main():
    """
    the function lets the user to play one game,
    then replays while the user wants, else exits the loops
    """
    words_list = load_words()
    type_input = PLAY_AGAIN
    replay = True
    while type_input != PLAY_AGAIN or replay == True:
        if type_input == PLAY_AGAIN:
            run_single_game(words_list)
        type_input, replay = get_input()

def update_word_pattern(word, pattern, letter):
    """
    :param word: gets a word (string) which
        the pattern should be updated against
    :param letter: gets a letter (string)
    :param pattern: gets the current pattern of the user (string)
    :return: returns updated pattern if needed
    """
    for i in range(len(word)):
        if word[i] == letter:
            # pattern[i] = letter
            pattern = pattern[:i] + letter + pattern[i+1:]
    return pattern

def run_single_game(words_list):
    """
    :param words_list: gets a list of words
    the function inits all variables,
    does the main loop and handles win and loss in the end of the game
    """
    chosen_word = get_random_word(words_list)
    pattern = HIDDEN_LETTER * len(chosen_word)
    wrong_guesses = []; correct_guesses = []
    msg = DEFAULT_MSG

    while game_over(chosen_word, pattern, wrong_guesses) == False:
        display_state(pattern, len(wrong_guesses),
                                     wrong_guesses, msg)
        type_input, user_input = get_input()
        msg = update_msg(words_list, correct_guesses, type_input,
                         user_input, pattern, wrong_guesses)
        pattern = update_pattern_guesses(chosen_word, correct_guesses,
                                         user_input, pattern, wrong_guesses)

    handle_game_over(chosen_word, pattern, wrong_guesses)


def handle_game_over(chosen_word, pattern, wrong_guesses):
    """
    the function prints if the user won or lost
    :param chosen_word: gets the word (string) the user had to guess
    :param pattern: gets the user pattern at the moment that he lost (string)
    :param wrong_guesses: gets the wrong guesses of the user
                    (list of string letters)
    """
    if pattern == chosen_word:
        msg = WIN_MSG
    else:
        msg = LOSS_MSG + chosen_word
    display_state(pattern, len(wrong_guesses), wrong_guesses, msg, True)


def game_over(word, pattern, wrong_guesses):
    """
    :param word: gets the chosen word (string)
    :param pattern: gets the current pattern (string)
    :param wrong_guesses: gets the current wrong guesses
                    (list of string letters)
    :return: if the game is over:
    if the wrong guesses is bigger of equal the max guesses or
            if the user guessed the word
    """
    return len(wrong_guesses) >= MAX_ERRORS or word == pattern

def update_msg(words_list, correct_guesses, type_input,
               letter, pattern, wrong_guesses):
    """
    :param words_list: gets a list of all words in the hangman (strings)
    :param correct_guesses:gets a list of letter strings of the correct guesses
    :param type_input: gets a type of input: play again, hint, letter
    :param letter: gets an input from the user (most likely a letter)
    :param pattern: gets the current pattern of the user (string)
    :param wrong_guesses: gets a list of letter strings of the wrong guesses
    :return: a new MSG to show the user based on the user's input
    """
    if type_input == HINT:
        filtered_list = filter_words_list(words_list, pattern, wrong_guesses)
        msg = HINT_MSG + choose_letter(filtered_list, pattern)
    elif letter not in LETTERS:
        msg = NON_VALID_MSG
    elif letter in correct_guesses or letter in wrong_guesses:
        msg = ALREADY_CHOSEN_MSG + letter
    else:
        msg = DEFAULT_MSG
    return msg

def update_pattern_guesses(chosen_word, correct_guesses,
                           letter, pattern, wrong_guesses):
    """
    :param chosen_word: gets the word (string) that the user should guess
    :param correct_guesses:gets a list of letter strings of the correct guesses
    :param letter: gets a letter from user(string)
    :param pattern: gets the current pattern of the user (string)
    :param wrong_guesses: gets a list of letter strings of the wrong guesses
    :return: the updated pattern based on the input
            and updates the guesses correctly
    """
    if letter not in LETTERS:
        return pattern
    #else if it is a letter the user already guessed
    if letter in correct_guesses or letter in wrong_guesses:
        return pattern
    #if it is a new letter and in the word
    if letter in chosen_word:
        correct_guesses.append(letter) # update the correct guess
        return update_word_pattern(chosen_word, pattern, letter)
    else: # if it a wrong guess
        wrong_guesses.append(letter)
        return pattern

def choose_letter(words_list, pattern):
    """
    :param words_list: gets a list of words that meet all requirements
    :param pattern: gets the current pattern of the user (string)
    :return: a char that appears the most in
            all the words and not in the pattern
    """
    lst = create_list_choose_letter(pattern)
    for word in words_list:
        for letter in word:
            # if it isn't a letter in the pattern
            if lst[convert_letter_to_index(letter)] > IGNORE_NUM:
                lst[convert_letter_to_index(letter)] += INC_NUM
    # find the index of the value that returned the most in the list
    max_index = get_index_of_max(lst)
    # convert that index back to a letter
    return convert_index_to_letter(max_index)

def convert_letter_to_index(letter):
    """
    :param letter: gets a string containing a letter
    :return: returns the index of the letter
        in the array and place in place of a:
    a = 0, b = 1, ...
    """
    return ord(letter) - ORD_A

def convert_index_to_letter(index):
    """
    :param letter: gets an index and converts it to a letter
    :return: returns the letter corresponding to the index:
    0 = a, 1 = b, ...
    """
    return chr(index + ORD_A)

def get_index_of_max(lst):
    """
    :param lst: gets a list of int
    :return: returns the index of the max int in the list
    """
    max_value = max(lst) #find the max value
    for i in range(len(lst)):
        if lst[i] == max_value:
            return i

def create_list_choose_letter(pattern):
    """
    :param pattern: gets the current pattern of the user (string)
    :return: creates a list with 25 places each
            place is 0 if the letter is not in pattern else 1
    """
    lst = list()
    for letter in LETTERS:
        if letter in pattern:
            lst.append(IGNORE_NUM)
        else:
            lst.append(RESET_NUM)
    return lst

def filter_words_list(words, pattern, wrong_guesses):
    """
    the function gets a list of words and requirements and
        returns a list of all words that meet all requirements
    :param words: gets a list of words to check which meet all requirements
    :param pattern: gets the current pattern of the user (string)
    :param wrong_guesses: gets a list of wrong guesses
                (containing letter strings)
    :return: a list of all words that meet all requirements
    """
    filtered_words = list()
    for word in words:
        if word_meets_all_requirements(word, pattern, wrong_guesses):
            filtered_words.append(word)
    return filtered_words

def wrong_guess_in_word(word, wrong_guesses):
    """
    the function returns true if the word has a wrong guess in it
    :param word: gets a word to check (string)
    :param wrong_guesses: gets a list of wrong guesses
                (containing letter strings)
    :return: returns true if the word CONTAINS a wrong_guess in it, else false
    """
    for wrong_guess in wrong_guesses:
        if wrong_guess in word:
            return True
    return False

def correct_guesses_in_correct_places(word, pattern):
    """
    the function determines if the word fits the pattern
    :param word: gets a word to check (string)
    :param pattern: gets the current pattern of the user (string)
    :return: returns true if the word fits the pattern
    """
    for letter in LETTERS:
        if letter in pattern:
            if correct_place_letter_pattern(word, pattern,  letter) == False:
                return False
    return True

def correct_place_letter_pattern(word, pattern, letter):
    """
    the function determines if the word fits the pattern
        only for the input letter
    :param word: gets a word to check (string)
    :param pattern: gets the current pattern of the user (string)
    :param letter: gets a letter of the abc (string)
    :return: returns true if the word fits the pattern for the input letter
    """
    for i in range(len(word)):
        if word[i] == letter:
            # word[i] == letter and letter != pattern[i],
            #  i.e. if the word doesn't fit the pattern
            if word[i] != pattern[i]:
                return False
        elif pattern[i] == letter: # word[i] != letter and letter == pattern[i]
            return False
    return True

def word_meets_all_requirements(word, pattern, wrong_guesses):
    """
    the function gets a string and few requirements, it returns
        if the word passes ALL requirements:
    1. the length of the pattern == the length of the word
    2. no wrong guess is in word
    3. the word fits the pattern
    :param word: gets a word to check (string)
    :param pattern: gets the current pattern of the user (string)
    :param wrong_guesses: gets a list of wrong guesses
        (containing letter strings)
    :return: returns true if the word meets all the defined
        requirements else false
    """
    return len(word) == len(pattern) and \
        wrong_guess_in_word(word, wrong_guesses) == False \
        and correct_guesses_in_correct_places(word, pattern) == True


if __name__ == '__main__':
    start_gui_and_call_main(main)
    close_gui()


