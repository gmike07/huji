from util import Pair


class ActionLayer(object):
    """
    A class for an ActionLayer in a level of the graph.
    The layer contains a set of actions (action objects) and a set of mutex actions (Pair objects)
    """

    def __init__(self):
        """
        Constructor
        """
        self.actions = set()  # set of all the actions in the layer
        self.mutexActions = set()  # set of pairs of action that are mutex in the layer

    def add_action(self, act):  # adds the action act to the actions set
        self.actions.add(act)

    def remove_actions(self, act):  # removes the action act to the actions set
        self.actions.remove(act)

    def get_actions(self):  # returns the actions set
        return self.actions

    def get_mutex_actions(self):  # returns the mutex actions set
        return self.mutexActions

    def add_mutex_actions(self, a1, a2):  # add the pair (a1,a2) to the mutex actions set
        self.mutexActions.add(Pair(a1, a2))

    def is_mutex(self, pair):
        """
        Returns true if the pair of actions are mutex in this action layer
        """
        return pair in self.mutexActions

    def effect_exists(self, prop):
        """
        Returns true if at least one of the actions in this layer has the proposition prop in its add list
        """
        for act in self.actions:
            if prop in act.get_add():
                return True
        return False

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
