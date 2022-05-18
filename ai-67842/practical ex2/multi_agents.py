import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)
        current_game_state = current_game_state.generate_successor(action=action)
        board = current_game_state.board
        max_tile = current_game_state.max_tile
        score = current_game_state.score
        score = np.log2(score) if score != 0 else 0
        # stuff about heuristics
        empty = np.sum(board == 0)

        # monotic
        mono1, merges1 = calculate_monotonic_merges(board)
        mono2, merges2 = calculate_monotonic_merges(board.T)
        mono, merges = mono1 + mono2, merges1 + merges2

        # if the max is not in the corner
        options = [board[0, 0], board[0, -1], board[-1, 0], board[-1, -1]]
        penalty1 = np.log2(max_tile) * (max_tile not in options)
        # if there are more than 2 times the same tile
        unique, counts = np.unique(board, return_counts=True)
        mask = (counts > 2) & (unique != 0)
        arr = (unique * counts)[mask]
        penalty2 = np.log2(np.max(arr)) if len(arr) != 0 else 0

        line_board = board.reshape((-1, 1))
        snakey_like = np.max(np.sum((weights * line_board), axis=0))
        snakey_like = np.log2(snakey_like) if snakey_like != 0 else 0

        sums = np.log2(np.sum(unique))

        penalty3 = 1000 * bool(
            len(current_game_state.get_agent_legal_actions()) == 0)

        average_tile = score / (16 - empty) if empty != 16 else 0

        # bonus_penalty = 2.5 if max_tile > 1024 else 0
        return 0.2 * score + 1.1 * empty - penalty1 - penalty2 - 1.4 * mono + \
               merges + snakey_like + sums + 1.1 * average_tile - penalty3 + \
               1.8 * max_tile


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def minimax(self, state, depth, is_max=True):
        if depth == 0:
            return Action.STOP, self.evaluation_function(state)
        actions = state.get_agent_legal_actions() if is_max else \
                  state.get_opponent_legal_actions()
        if len(actions) == 0:
            return Action.STOP, self.evaluation_function(state)
        if is_max:
            max_action, max_score = Action.STOP, -float('inf')
            for action in actions:
                new_state = state.generate_successor(agent_index=0, action=action)
                prev_action, score = self.minimax(new_state, depth, False)
                if score > max_score:
                    max_action, max_score = action, score
            return max_action, max_score
        else:
            min_action, min_score = Action.STOP, float('inf')
            for action in actions:
                new_state = state.generate_successor(agent_index=1, action=action)
                prev_action, score = self.minimax(new_state, depth - 1, True)
                if score < min_score:
                    min_action, min_score = action, score
            return min_action, min_score


    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        action, score = self.minimax(game_state, self.depth)
        return action



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def minimax(self, state, depth, is_max=True, alpha=-float('inf'),
                beta=float('inf')):
        if depth == 0:
            return Action.STOP, self.evaluation_function(state)
        actions = state.get_agent_legal_actions() if is_max else \
                  state.get_opponent_legal_actions()
        if len(actions) == 0:
            return Action.STOP, self.evaluation_function(state)
        best_action = Action.STOP
        if is_max:
            for action in actions:
                new_state = state.generate_successor(agent_index=0, action=action)
                prev_action, score = self.minimax(new_state, depth, False,
                                                  alpha, beta)
                if alpha < score:
                    best_action, alpha = action, score
                if alpha >= beta:
                    return best_action, alpha
            return best_action, alpha
        else:
            for action in actions:
                new_state = state.generate_successor(agent_index=1, action=action)
                prev_action, score = self.minimax(new_state, depth - 1, True, alpha, beta)
                if score < beta:
                    best_action, beta = action, score
                if alpha >= beta:
                    return best_action, beta
            return best_action, beta


    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, score = self.minimax(game_state, self.depth)
        return action



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def expectimax(self, state, depth, is_max=True):
        if depth == 0:
            return Action.STOP, self.evaluation_function(state)
        actions = state.get_agent_legal_actions() if is_max else \
                  state.get_opponent_legal_actions()
        if len(actions) == 0:
            return Action.STOP, self.evaluation_function(state)
        best_action, best_score = Action.STOP, -float('inf')
        if is_max:
            for action in actions:
                new_state = state.generate_successor(agent_index=0, action=action)
                prev_action, score = self.expectimax(new_state, depth, False)
                if best_score < score:
                    best_action, best_score = action, score
            return best_action, best_score
        else:
            sum_score = 0
            for action in actions:
                new_state = state.generate_successor(agent_index=1, action=action)
                prev_action, score = self.expectimax(new_state, depth - 1, True)
                sum_score += score
            return Action.STOP, sum_score / len(actions)

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        action, score = self.expectimax(game_state, self.depth)
        return action


weights1 = np.array([[16, 15, 14, 13],
                     [9, 10, 11 ,12],
                     [8, 7, 6, 5],
                     [1, 2, 3, 4]])
weights2 = weights1.T
weights3 = np.array([[13, 14, 15, 16],
                     [12, 11, 10, 9],
                     [5, 6, 7, 8],
                     [4, 3, 2, 1]])
weights4 = weights3.T
weights5 = np.array([[1, 2, 3, 4],
                     [8, 7, 6, 5],
                     [9, 10, 11, 12],
                     [16, 15, 14, 13]])
weights6 = weights5.T

weights7 = np.array([[4, 3, 2, 1],
                     [5, 6, 7, 8],
                     [12, 11, 10, 9],
                     [13, 14, 15, 16]])
weights8 = weights7.T

weights = np.array([weights1.ravel(), weights2.ravel(), weights3.ravel(),
                    weights4.ravel(), weights5.ravel(), weights6.ravel(),
                    weights7.ravel(), weights8.ravel()]).T


def calculate_monotonic_merges(board):
    board1, board2 = board[1:], board[:-1]
    helper = board2 - board1
    mask = ((board1 != 0) | (board2 != 0)) & (helper == 0)
    merges = np.sum(mask, axis=1)
    merges = np.sum(merges) + np.sum(merges > 0)

    sum_pos = np.sum(helper * (helper > 0))
    sum_neg = -np.sum(helper * (helper < 0))
    mono = min(np.sum(sum_pos), np.sum(sum_neg))
    return np.log2(mono) if mono != 0 else 0, merges


def snake_monotonic(board):
    monotonic = board[:, :]
    monotonic[1::2] = monotonic[1::2, ::-1]
    snake1 = monotonic.ravel()
    snake1 = np.diff(snake1) * (snake1[1:] != 0) * (snake1[:-1] != 0)
    monotonic = monotonic[::-1]
    snake2 = monotonic.ravel()
    snake2 = np.diff(snake2) * (snake2[1:] != 0) * (snake2[:-1] != 0)
    mono = min(np.sum(np.abs(snake1 * (snake1 > 0))),
               np.sum(np.abs(snake1 * (snake1 < 0))),
               np.sum(np.abs(snake2 * (snake2 > 0))),
               np.sum(np.abs(snake2 * (snake2 < 0))))
    return np.log2(mono) if mono != 0 else 0


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    board = current_game_state.board
    max_tile = current_game_state.max_tile
    score = current_game_state.score
    score = np.log2(score) if score != 0 else 0
    # stuff about heuristics
    empty = np.sum(board == 0)

    #monotic
    mono1, merges1 = calculate_monotonic_merges(board)
    mono2, merges2 = calculate_monotonic_merges(board.T)
    mono, merges = mono1 + mono2, merges1 + merges2

    # if the max is not in the corner
    options = [board[0, 0], board[0, -1], board[-1, 0], board[-1, -1]]
    penalty1 = np.log2(max_tile) * (max_tile not in options)
    penalty1 = 20 * penalty1 if penalty1 > 7 else penalty1
    penalty1 = 4 * penalty1 if penalty1 > 9 else penalty1
    # if there are more than 2 times the same tile
    unique, counts = np.unique(board, return_counts=True)
    mask = (counts > 2) & (unique != 0)
    arr = (unique * counts)[mask]
    penalty2 = np.log2(np.max(arr)) if len(arr) != 0 else 0

    line_board = board.reshape((-1, 1))
    snakey_like = np.max(np.sum((weights * line_board), axis=0))
    snakey_like = np.log2(snakey_like) if snakey_like != 0 else 0

    sums = np.log2(np.sum(unique))

    penalty3 = 1000 * bool(len(current_game_state.get_agent_legal_actions()) == 0)

    average_tile = np.log2(np.sum(board)) / (16 - empty) if empty != 16 else 0

    s2, s4 = np.sum(board == 2), np.sum(board == 4)
    penalty4 = 0
    if s2 > 2:
        penalty4 += s2 - 2
    if s4 > 2:
        penalty4 += s4 - 2

    mono_snake = min(snake_monotonic(board), snake_monotonic(board.T))
    # bonus_penalty = 2.5 if max_tile > 1024 else 0
    return 0.1 * score + 1.1 * empty - 3 * penalty1 - penalty2 - 2.1 * mono + \
           merges + snakey_like + sums + 1.3 * average_tile - penalty3 + \
           1.8 * max_tile - 0.05 * penalty4 - 0.15 * mono_snake


# Abbreviation
better = better_evaluation_function
