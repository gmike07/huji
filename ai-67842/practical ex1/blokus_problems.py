import math

from board import Board
from search import SearchProblem, ucs, astar, greedy_best_search, \
    a_star_search_banned
import util
import numpy as np

helper_dct = {(a, b): {(a, b)} for a in [-1.0, 1.0] for b in [-1.0, 1.0]}
helper_dct = {**{(0.0, b): {(a, b)} for a in [-1.0, 0.0, 1.0] for b in [-1.0, 1.0]}, **helper_dct}
helper_dct = {**{(a, 0.0): {(a, b)} for a in [-1.0, 1.0] for b in [-1.0, 0.0, 1.0]}, **helper_dct}
helper_dct = {**{(0.0, 0.0): {(a, b)} for a in [-1.0, 0.0, 1.0] for b in [-1.0, 0.0, 1.0]}, **helper_dct}


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0
        self.targets = [(0, 0), (0, board_w-1), (board_h-1, 0), (board_h-1, board_w-1)]
        self.pieces = np.array([piece.get_num_tiles() for piece in piece_list])

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        return state.state[0, 0] != -1 and state.state[-1, 0] != -1 \
               and state.state[0, -1] != -1 and state.state[-1, -1] != -1

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles())
                for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(action.piece.get_num_tiles() for action in actions)


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    tars = problem.targets
    free_targets = [target for target in tars if state.state[target] == -1]
    count_targets = len(free_targets)
    # if solution
    if count_targets == 0:
        return 0

    max_dist = 0
    y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
    # if we don't have a place to place new targets then there is no solution
    if len(x_lst) == 0 or not np.any(state.pieces[0]):
        return float('inf')

    target_distance = {target: -1 for target in tars}
    # find max distance and the direction vector to it
    for target in free_targets:
        y_target, x_target = target
        y_abs = np.abs(y_lst - y_target)
        x_abs = np.abs(x_lst - x_target)

        curr = np.min(np.maximum(y_abs, x_abs))
        target_distance[target] = curr

        max_dist = max(max_dist, curr)

    #check if we can use the best heuristic
    dist = float('inf')
    for i in range(len(free_targets)):
        y_target, x_target = free_targets[i]
        for j in range(i + 1, len(free_targets)):
            y_other, x_other = free_targets[j]
            dist = min(dist, max(abs(y_target - y_other),
                                 abs(x_target - x_other)))

    # sum of opposite corners distance is admissble
    s = 0
    if tars[0] in free_targets and tars[3] in free_targets:
        d1, d2 = target_distance[tars[0]], target_distance[tars[3]]
        s = max(d1 + d2 + 1, s)
    if tars[1] in free_targets and tars[2] in free_targets:
        d1, d2 = target_distance[tars[1]], target_distance[tars[2]]
        s = max(d1 + d2 + 1, s)

    # return the max of (max dist, targets left, max dist + targets left,
    # sum of targets left minimal pieces in the game, diagonal sum)
    lst = problem.pieces * state.pieces[0]
    if dist >= max(lst) and len(lst) >= count_targets:
        lst[lst == 0] = 1000
        lst = np.append(lst, 1000)
        return max(max_dist, count_targets, max_dist + count_targets, s,
            np.sum(lst[np.argpartition(lst, count_targets)[:count_targets]]))
    return max(max_dist, count_targets, max_dist + count_targets, s)


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.pieces = np.array([piece.get_num_tiles() for piece in piece_list])
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.state[target] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles())
                for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This  method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(action.piece.get_num_tiles() for action in actions)


def blokus_cover_heuristic(state, problem):
    tars = problem.targets
    free_targets = [target for target in tars if state.state[target] == -1]
    count_targets = len(free_targets)
    #if solution
    if count_targets == 0:
        return 0

    # if there is no solution from this state because we can't fill targets
    for target in free_targets:
        y, x = target
        if not state._legal[0, y, x]:
            return float('inf')

    # if we don't have a place to place new targets then there is no solution
    max_dist = 0
    y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
    if len(x_lst) == 0 or not np.any(state.pieces[0]):
        return float('inf')


    best_index = -1
    signs = (1, 1)
    #preform calculations
    for target in free_targets:
        y_target, x_target = target
        y_abs = np.abs(y_lst - y_target)
        x_abs = np.abs(x_lst - x_target)
        curr_index = np.argmin(np.maximum(y_abs, x_abs))
        curr = max(y_abs[curr_index], x_abs[curr_index]) + 1
        if curr > max_dist:
            best_index = curr_index
            signs = (np.sign(y_lst[curr_index] - y_target),
                     np.sign(x_lst[curr_index] - x_target))
        max_dist = max(max_dist, curr)

    count_in_way = 0
    signs = helper_dct[signs]
    # check if we can use the best heuristic
    dist = float('inf')
    for i in range(len(free_targets)):
        y_target, x_target = free_targets[i]
        if helper_dct[(np.sign(y_lst[best_index] - y_target),
                       np.sign(x_lst[best_index] - x_target))] \
                & signs != set():
            count_in_way += 1
        for j in range(i + 1, len(free_targets)):
            y_other, x_other = free_targets[j]
            dist = min(dist, max(abs(y_target - y_other), abs(x_target - x_other)))

    # return the max of (max dist, targets left, max dist + targets left - in way,
    # sum of targets left minimal pieces in the game, diagonal sum)
    lst = problem.pieces * state.pieces[0]
    if dist >= max(lst) and len(lst) >= count_targets:
        lst[lst == 0] = 1000
        lst = np.append(lst, 1000)
        return max(max_dist, count_targets, max_dist + count_targets - count_in_way,
                   np.sum(lst[np.argpartition(lst, count_targets)[:count_targets]]))
    return max(max_dist, count_targets, max_dist + count_targets - count_in_way,
               min(piece.get_num_tiles() for i, piece in enumerate(state.piece_list) if state.pieces[0, i]))


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.starting_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def get_closest_target(self, board, targets):
        min_dist = float('inf')
        y_lst, x_lst = np.nonzero(np.logical_and(board.connected[0], board._legal[0]))
        best_index, best_target = -1, -1
        for target in targets:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr_i = np.argmin(np.maximum(y_abs, x_abs))
            curr_dist = max(y_abs[curr_i], x_abs[curr_i]) + 1
            if min_dist > curr_dist:
                min_dist = curr_dist
                best_index, best_target = curr_i, target
        return (y_lst[best_index], x_lst[best_index]), best_target


    def solve_recursive(self, state, targets):
        if len(targets) == 0:
            return []
        invalid_moves = set()
        for target in targets:
            y, x = target
            if not state._legal[0, y, x]:
                return None
        point, curr_target = self.get_closest_target(state, targets)
        problem = BlokusCoverProblem(state.board_w, state.board_h,
                                     state.piece_list,
                                     point, [curr_target])
        problem.board = state
        actions = a_star_search_banned(problem, invalid_moves, blokus_cover_heuristic)
        while actions is not None:
            self.expanded += problem.expanded
            curr_state = state
            for action in actions:
                curr_state = curr_state.do_move(0, action)
            new_targets = [target for target in targets if curr_state.state[target] == -1
                           and curr_target != target]
            backtrace = self.solve_recursive(curr_state, new_targets)
            if backtrace is not None:
                actions.extend(backtrace)
                return actions
            invalid_moves.add(curr_state)
            problem.expanded = 0
            actions = a_star_search_banned(problem, invalid_moves, blokus_cover_heuristic)

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        curr_state = self.board.__copy__()
        return self.solve_recursive(curr_state, self.targets)


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    @staticmethod
    def heuristic(state, problem):
        tars = problem.targets
        free_targets = [target for target in tars if state.state[target] == -1]
        count_targets = len(free_targets)
        if count_targets == 0:
            return 0

        y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
        if len(x_lst) == 0 or not np.any(state.pieces[0]):
            return float('inf')

        sett = set()
        sum_dist = 0
        for target in free_targets:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr_index = np.argmin(np.maximum(y_abs, x_abs))
            curr = max(y_abs[curr_index], x_abs[curr_index])
            if all(curr != max(y,x) for (y, x) in sett):
                sett.add((y_lst[curr_index], x_lst[curr_index]))
            sum_dist += np.min(y_abs + x_abs) + 1
        return sum_dist + (count_targets - len(sett))


    def is_goal_state(self, state):
        for target in self.targets:
            if state.state[target] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded += 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles())
                for move in state.get_legal_moves(0)]

    def solve(self):
        "*** YOUR CODE HERE ***"
        return astar(self, MiniContestSearch.heuristic)











#FAILED HEURISTICS
def calc_cost(state, problem):
    # lst = problem.pieces * state.pieces[0]
    # lst[lst == 0] = 1000
    # num = sum(1 for target in problem.targets if state.state[target] == -1)
    #
    # return np.sum(lst[np.argpartition(lst, num)[:num]])
    max_dist = 0
    y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
    if len(x_lst) == 0:
        return float('inf')

    count_targets = 0
    sum_dist = 0
    free_targets = []
    for target in problem.targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr = np.min(np.maximum(y_abs, x_abs))
            max_dist = max(max_dist, curr)
            sum_dist += curr + 1
            count_targets += 1
            free_targets.append(target)
    if count_targets == 0:
        return 0
    dist = float('inf')
    for i in range(len(free_targets)):
        y_target, x_target = free_targets[i]
        for j in range(i + 1, len(free_targets)):
            y_other, x_other = free_targets[j]
            dist = min(dist, max(abs(y_target - y_other), abs(x_target - x_other)))
    if not ((state.state[0, 0] != -1 and state.state[-1, -1] != -1) or
            (state.state[0, -1] != -1 and state.state[-1, 0] != -1)):
        sum_dist = math.floor(sum_dist / 2)
    lst = problem.pieces * state.pieces[0]
    if dist >= max(lst):
        lst[lst == 0] = 1000
        return max(np.sum(lst[np.argpartition(lst, count_targets)[:count_targets]]),
                   max_dist, count_targets, max_dist + count_targets, sum_dist)
    return max(max_dist, count_targets, max_dist + count_targets, sum_dist)

    max_dist = 0

    # ------ NEW HEURISTIC -----
    y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
    if len(x_lst) == 0:
        return float('inf')

    count_targets = 0
    sum_dist = 0
    for target in targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr = np.min(np.maximum(y_abs, x_abs))
            max_dist = max(max_dist, curr)
            sum_dist += curr + 1
            count_targets += 1
    if count_targets == 0:
        return 0
    if not ((state.state[0, 0] != -1 and state.state[-1, -1] != -1) or
            (state.state[0, -1] != -1 and state.state[-1, 0] != -1)):
        sum_dist = math.floor(sum_dist / 2)
    sorted_arr = sorted(piece.get_num_tiles() for i, piece in enumerate(state.piece_list) if state.pieces[0, i])
    return max(sum(sorted_arr[:count_targets]), max_dist,
               count_targets, max_dist + count_targets-1, sum_dist)  # , m + count_targets, dst, max_dist_man)
    dict = {}
    points = []
    for target in targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr_dis = np.maximum(y_abs,x_abs)
            curr_point = np.argmin(curr_dis)
            y = y_abs[curr_point]
            x = x_abs[curr_point]
            curr_point = (y_lst[curr_point], x_lst[curr_point])
            points.append(curr_point)
            dict[target] = (y, x)
        else:
            dict[target] = (0, 0)
            points.append((-1,-1))
    sum_dis = len(list(set(points).difference({(-1,-1)})))

    if points[0] == points[2] and points[0] != (-1,-1) :
        y, x =   dict[(0, 0)]
        # print(y,x)
        dict[(0, 0)]= (y,0)
    if points[1] == points[3] and points[1] != (-1,-1) :
        y, x = dict[(0, state.board_w-1)]
        dict[(0, state.board_w-1)] = (y, 0)
    for target in dict.keys():
        sum_dis += max(dict[target][1],  dict[target][0])
    return  sum_dis

    # ------ END NEW HEURISTIC -----


    count_targets = 0
    sum_dist = 0
    max_dist_man = 0
    # dir_y = {'UP': 0, 'DOWN': 0, 0: 0}
    # dir_x = {'UP': 0, 'DOWN': 0, 0: 0}
    for target in targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)

            # index_curr = np.argmin(np.maximum(y_abs, x_abs))
            curr = np.min(np.maximum(y_abs, x_abs)) + 1
            # if y_abs[index_curr] == curr:
            #     if curr - y_target - 1 > 0:
            #         dir_y['UP'] += 1
            #     if curr - y_target - 1 < 0:
            #         dir_y['DOWN'] += 1
            # else:
            #     if curr - x_target - 1 > 0:
            #         dir_y['UP'] += 1
            #     if curr - x_target - 1 < 0:
            #         dir_y['DOWN'] += 1
            max_dist = max(max_dist, curr)
            max_dist_man = max(max_dist_man, np.min(y_abs + x_abs) + 1)
            sum_dist += curr
            count_targets += 1

    # print(dir_x, dir_y)
    if not ((state.state[0, 0] != -1 and state.state[-1, -1] != -1) or
        (state.state[0, -1] != -1 and state.state[-1, 0] != -1)):
        sum_dist = math.floor(sum_dist / 2)
    if count_targets == 0:
        return 0
    dst = 2 * max(state.board_h, state.board_w) - np.count_nonzero(state.state == 0)
    return max(sum_dist, max_dist, count_targets, max_dist + count_targets - 1,
               min(piece.get_num_tiles() for piece in state.piece_list)) #, m + count_targets, dst, max_dist_man)
    sum_dist = 0
    max_dist = 0
    y_lst, x_lst = np.nonzero(state.connected[0, :, :])
    count_targets = 0

    dct_target_x = {'FOR': 0, 'BACK': 0}
    dct_target_y = {'FOR': 0, 'BACK': 0}
    exists = []
    for target in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
        if state.state[target] == -1:
            exists.append(state)
    mapping = {0: 0, 2: 1, 1: 2}
    for target in targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            # y_abs = (y_lst - y_target)
            # x_abs = (x_lst - x_target)
            # if exists == [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
            #     pass
            # dct_target_x[target] = (np.min(abs(x_abs))+1, np.sign(x_abs))
            # dct_target_y[target] = (np.min(abs(y_abs))+1, np.sign(y_abs))
            curr = np.min(np.maximum((mapping[max(dct_target_y.values())])*y_abs, (mapping[max(dct_target_x.values())])* x_abs)) + 1
            sum_dist += curr
            count_targets += 1
            max_dist = max(max_dist, curr)
    x_dct = {1: 0, -1: 0}
    y_dct = {1: 0, -1: 0}
    for target in dct_target_x.keys():
        x_dct[dct_target_x[target][1]] += dct_target_x[target][0]
        y_dct[dct_target_y[target][1]] += dct_target_y[target][0]

    return max(math.floor(sum_dist / 2), count_targets, max_dist)






    if not np.any(state.pieces[0]):
        return float('inf')
    max_dist = 0
    y_lst, x_lst = np.nonzero(state.connected[0] & state._legal[0])
    if len(x_lst) == 0:
        return float('inf')

    count_targets = 0
    sum_dist = 0
    free_targets = []
    for target in problem.targets:
        if state.state[target] == -1:
            y_target, x_target = target
            y_abs = np.abs(y_lst - y_target)
            x_abs = np.abs(x_lst - x_target)
            curr = np.min(np.maximum(y_abs, x_abs))
            max_dist = max(max_dist, curr)
            sum_dist += curr + 1
            count_targets += 1
            free_targets.append(target)
    if count_targets == 0:
        return 0
    dist = float('inf')
    for i in range(len(free_targets)):
        y_target, x_target = free_targets[i]
        for j in range(i + 1, len(free_targets)):
            y_other, x_other = free_targets[j]
            dist = min(dist, max(abs(y_target - y_other), abs(x_target - x_other)))
    if not ((state.state[0, 0] != -1 and state.state[-1, -1] != -1) or
            (state.state[0, -1] != -1 and state.state[-1, 0] != -1)):
        sum_dist = math.floor(sum_dist / 2)
    if dist >= 5:
        sorted_arr = sorted(piece.get_num_tiles() for i, piece in
                            enumerate(state.piece_list) if state.pieces[0, i])
        return max(sum(sorted_arr[: count_targets]), max_dist,
                   count_targets, max_dist + count_targets, sum_dist)
    return max(max_dist, count_targets, max_dist + count_targets, sum_dist)