import abc
from collections import namedtuple
from enum import Enum

import numpy as np
import time


class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5


OpponentAction = namedtuple('OpponentAction', ['row', 'column', 'value'])


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass


class RandomOpponentAgent(Agent):
    FOUR_VS_TWO_PROB = 0.1

    def get_action(self, game_state):
        empty_tiles = game_state.get_empty_tiles()
        tile_index = np.random.choice(empty_tiles[0].size)
        value = 2
        if np.random.uniform() <= RandomOpponentAgent.FOUR_VS_TWO_PROB:
            value = 4
        return OpponentAction(row=empty_tiles[0][tile_index], column=empty_tiles[1][tile_index], value=value)


class Game(object):
    def __init__(self, agent, opponent_agent, display, sleep_between_actions=False):
        super(Game, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = None
        self._should_quit = False

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.agent.stop_running()
        self.opponent_agent.stop_running()

    def _game_loop(self):
        while not self._state.done and not self._should_quit:
            if self.sleep_between_actions:
                time.sleep(1)
            self.display.mainloop_iteration()
            action = self.agent.get_action(self._state)
            if action == Action.STOP:
                return
            self._state.apply_action(action)
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            self.display.update_state(self._state, action, opponent_action)
        return self._state.score, self._state.max_tile
