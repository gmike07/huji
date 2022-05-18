import argparse
import numpy
import os
import util
from game import Game, RandomOpponentAgent
from game_state import GameState
from graphics_display import GabrieleCirulli2048GraphicsDisplay
from keyboard_agent import KeyboardAgent

NUM_OF_INITIAL_TILES = 2


class GameRunner(object):
    def __init__(self, display=None, agent=None, num_of_initial_tiles=NUM_OF_INITIAL_TILES,
                 sleep_between_actions=False):
        super(GameRunner, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.num_of_initial_tiles = num_of_initial_tiles
        self.human_agent = agent is None
        if display is None:
            display = GabrieleCirulli2048GraphicsDisplay(self.new_game, self.quit_game, self.human_agent)

        if agent is None:
            agent = KeyboardAgent(display)

        self.display = display
        self._agent = agent
        self.current_game = None

    def new_game(self, initial_state=None, *args, **kw):
        self.quit_game()
        if initial_state is None:
            initial_state = GameState()
        opponent_agent = RandomOpponentAgent()
        game = Game(self._agent, opponent_agent, self.display, sleep_between_actions=self.sleep_between_actions)
        for i in range(self.num_of_initial_tiles):
            initial_state.apply_opponent_action(opponent_agent.get_action(initial_state))
        self.current_game = game
        return game.run(initial_state)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(args):
    if args.agent == 'ReflexAgent':
        from multi_agents import ReflexAgent
        agent = ReflexAgent()
    else:
        agent = util.lookup('multi_agents.' + args.agent, globals())(depth=args.depth,
                                                                     evaluation_function=args.evaluation_function)
    return agent


def main():
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'ReflexAgent', 'MinmaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default=displays[0], type=str)
    parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[0], type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--num_of_initial_tiles', help='The number non empty tiles when the game started.', default=2,
                        type=int)
    parser.add_argument('--initial_board', help='Initial board for new games.', default=None, type=str)
    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='score_evaluation_function', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    if args.display != displays[0]:
        display = util.lookup('displays.' + args.display, globals())()
    else:
        display = None
    if args.agent != agents[0]:
        agent = create_agent(args)
    else:
        agent = None
    initial_state = None
    if args.initial_board is not None:
        with open(os.path.join('layouts', args.initial_board), 'r') as f:
            lines = f.readlines()
            initial_board = numpy.array([list(map(lambda x: int(x), line.split(','))) for line in lines])
            initial_state = GameState(board=initial_board)
    game_runner = GameRunner(display=display, agent=agent, num_of_initial_tiles=args.num_of_initial_tiles,
                             sleep_between_actions=args.sleep_between_actions)
    for i in range(args.num_of_games):
        score = game_runner.new_game(initial_state=initial_state)
    if display is not None:
        display.print_stats()


if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
