from util import Pair


class PropositionLayer(object):
    """
    A class for an PropositionLayer  in a level of the graph.
    The layer contains a set of propositions (Proposition objects) and a set of mutex propositions (Pair objects)
    """

    def __init__(self):
        """
        Constructor
        """
        self.propositions = set()
        # set of all the propositions in the layer
        self.mutexPropositions = set()
        # set of pairs of propositions that are mutex in the layer

    def add_proposition(self, proposition):
        # adds proposition to the propositions set
        self.propositions.add(proposition)

    def remove_propositions(self, proposition):
        # remove proposition from the propositions set
        self.propositions.remove(proposition)

    def get_propositions(self):
        # returns the propositions set
        return self.propositions

    def add_mutex_prop(self, p1, p2):
        # adds the pair(p1,p2) to the mutex propositions set
        self.mutexPropositions.add(Pair(p1, p2))

    """
    returns true if proposition p1 and proposition p2 are mutex at this layer
    """

    def is_mutex(self, p1, p2):
        return Pair(p1, p2) in self.mutexPropositions

    def get_mutex_props(self):  # returns the mutex propositions set
        return self.mutexPropositions

    def all_preconds_in_layer(self, action):
        """
        returns true if all propositions that are preconditions of the
        action exist in this layer (i.e. the action can be applied)
        """
        action_pre = action.get_pre()
        for pre in action_pre:
            if not (pre in self.propositions):
                return False

        for i in range(len(action_pre)):
            for j in range(i + 1, len(action_pre)):
                pre1 = action_pre[i]
                pre2 = action_pre[j]
                if Pair(pre1, pre2) in self.mutexPropositions:
                    return False

        return True

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
