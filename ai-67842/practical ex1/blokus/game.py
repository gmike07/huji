from inputs import RandomInput
from pieces import PieceList
from blokus_problems import *
from search import astar
from displays import GuiDisplay
import sys
import os
import ast


class GameEngine(object):
    """
    Game engine class stores the current game state and controls when to
    get input/draw output
    """

    def __init__(self, inputs, width, height, piece_list):
        self.display = GuiDisplay(width, height, title='Intro to AI -- 67842 -- Ex1')
        self.inputs = inputs

        self.piece_list = piece_list

        self.num_players = len(inputs)
        self.board_w = width
        self.board_h = height
        self.turn_num = 0
        self.passed = [False] * self.num_players
        self.score = [0] * self.num_players
        self.board = Board(self.board_w, self.board_h, self.num_players, self.piece_list)

        # Set up initial corners for each player
        if self.num_players > 1:
            self.board.connected[1, 0, self.board_w - 1] = True
            if self.num_players > 2:
                self.board.connected[2, self.board_h - 1, 0] = True
                if self.num_players > 3:
                    self.board.connected[3, self.board_h - 1, self.board_h - 1] = True

    def play_turn(self):
        """
        Play a single round of turns.

        Check for empty moves from the inputs (signalling passes) and ask for 
        new moves if illegal moves are provided.
        """
        self.turn_num += 1
        # print "Starting turn %d" % self.turn_num

        for p in range(self.num_players):
            if self.passed[p]:
                continue

            self.display.draw_board(self.board)
            while True:
                move = self.inputs[p].get_move(p, self.board)
                if move is None:
                    self.passed[p] = True
                    break
                if not self.board.pieces[p, move.piece_index]:
                    print("Error: piece has already been used. Try again:")
                    continue
                try:
                    self.score[p] += self.board.add_move(p, move)
                    self.board.pieces[p, move.piece_index] = False
                    break
                except ValueError:
                    print("Error: move is illegal. Try again:")

    def all_players_passed(self):
        """
        Return True if all players have passed.
        """
        for p in range(self.num_players):
            if not self.passed[p]:
                return False
        return True

    def _print_scores(self):
        for p in range(self.num_players):
            print("Player %d: %d pts" % (p + 1, self.score[p]))

    def play_game(self):
        if len(self.inputs) != 4:
            print("Error: Need 4 players for a game. ")
            sys.exit(1)
        while not self.all_players_passed():
            self.play_turn()

        self._print_scores()
        return self.score


def play_simple_search(problem, search_func):
    back_trace = search_func(problem)
    display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- Ex1')
    board = problem.get_start_state()
    if problem.__class__ == BlokusCornersProblem:
        dots = [(board.board_h - 1, board.board_w - 1), (0, board.board_w - 1), (board.board_h - 1, 0)]
    else:
        try:
            dots = problem.targets
        except AttributeError:
            dots = []
    for action in back_trace:
        board.add_move(0, action)
        display.draw_board(board, dots=dots)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, board.score(0)))


def play_a_star_search(problem, heuristic):
    back_trace = astar(problem, heuristic)
    display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- Ex1')
    board = problem.get_start_state()

    if problem.__class__ == BlokusCornersProblem:
        dots = [(board.board_h - 1, board.board_w - 1), (0, board.board_w - 1), (board.board_h - 1, 0)]
    else:
        try:
            dots = problem.targets
        except AttributeError:
            dots = []

    for action in back_trace:
        board.add_move(0, action)
        display.draw_board(board, dots=dots)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, board.score(0)))


def play_approximate_search(problem):
    back_trace = problem.solve()
    display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- Ex1')
    board = problem.get_start_state()
    for action in back_trace:
        board.add_move(0, action)
        display.draw_board(board, dots=problem.targets)
    print("Expanded nodes: %d, score: %d" % (problem.expanded, board.score(0)))


def load_heuristic(heuristic_name):
    # Looks through all pythonPath Directories for the right function
    python_path_str = os.path.expandvars("$PYTHONPATH")
    if python_path_str.find(';') == -1:
        python_path_dirs = python_path_str.split(':')
    else:
        python_path_dirs = python_path_str.split(';')
    python_path_dirs.append('.')

    for moduleDir in python_path_dirs:
        if not os.path.isdir(moduleDir):
            continue
        module_names = [f for f in os.listdir(moduleDir) if os.path.isfile(f)]
        for module_name in module_names:
            try:
                module = __import__(str(module_name[:-3]))
            except ImportError:
                continue
            if heuristic_name in dir(module):
                return getattr(module, heuristic_name)
    raise Exception('The function ' + heuristic_name + ' was not found.')


def main():
    """
    Processes the command used to run the game from the command line.
    """
    from optparse import OptionParser
    usage_str = """
    USAGE:      python game.py <options>
    EXAMPLES:  (1) python game.py
                  - starts a game between 4 random agents
               (2) python game.py -p tiny_set.txt -s 4 7
               OR  python game.py -s 14 14 -f ucs -z cover [(1, 1), (5, 9), (9, 6)]
    """
    parser = OptionParser(usage_str)

    parser.add_option('-p', '--pieces', dest='pieces_file',
                      help='the file to read for the list of pieces',
                      default='valid_pieces.txt')
    parser.add_option('-s', '--board-size', dest='size',
                      type='int', nargs=2, help='the size of the game board.', default=(20, 20))
    parser.add_option('-f', '--search-function', dest='search_func',
                      metavar='FUNC', help='search function to use. This option is ignored for sub-optimal search. ',
                      type='choice',
                      choices=['dfs', 'bfs', 'ucs', 'astar'], default='dfs')
    parser.add_option('-H', '--heuristic', dest='h_func',
                      help='heuristic function to use for A* search. \
                      This option is ignored for other search functions. ',
                      metavar='FUNC', default=None)
    parser.add_option('-z', '--puzzle', dest='puzzle',
                      help='the type of puzzle being solved', type='choice',
                      choices=['fill', 'diagonal', 'corners', 'cover', 'sub-optimal', 'mini-contest'], default=None)
    parser.add_option('-x', '--start-point', dest='start', type='int', nargs=2,
                      help='starting point', default=(0, 0))

    options, cover_points = parser.parse_args()
    if (options.puzzle == 'cover' or options.puzzle == 'sub-optimal') and len(cover_points) == 0:
        raise Exception('cover puzzles require at least one point to cover!')

    if options.puzzle == 'cover' or options.puzzle == 'sub-optimal' or options.puzzle == 'mini-contest':
        targets = ast.literal_eval(''.join(cover_points))

    piece_list = PieceList(options.pieces_file)

    if options.puzzle is None:
        inputs = [RandomInput() for _ in range(4)]
        engine = GameEngine(inputs, options.size[1], options.size[0], piece_list)
        engine.play_game()

    elif options.puzzle == 'sub-optimal':
        problem = ClosestLocationSearch(options.size[1], options.size[0], piece_list, options.start, targets)
        play_approximate_search(problem)

    elif options.puzzle == 'mini-contest':
        problem = MiniContestSearch(options.size[1], options.size[0], piece_list, options.start, targets)
        play_approximate_search(problem)

    elif options.search_func in ['dfs', 'bfs', 'ucs', 'astar']:
        if options.puzzle == 'fill':
            problem = BlokusFillProblem(options.size[1], options.size[0], piece_list, options.start)
        elif options.puzzle == 'corners':
            problem = BlokusCornersProblem(options.size[1], options.size[0], piece_list, options.start)
        elif options.puzzle == 'cover':
            problem = BlokusCoverProblem(options.size[1], options.size[0], piece_list, options.start, targets)

        if options.search_func in ['dfs', 'bfs', 'ucs']:
            search = __import__('search')
            play_simple_search(problem, getattr(search, options.search_func))
        elif options.search_func == 'astar':
            play_a_star_search(problem, load_heuristic(options.h_func))
    else:
        raise Exception('unrecognized options')


if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
