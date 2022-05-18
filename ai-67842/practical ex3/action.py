class Action(object):
    """
    The action class is used to define operators.
    Each action has a list of preconditions, an "add list" of positive effects,
    a "delete list" for negative effects, and the name of the action.
    Two actions are considered equal if they have the same name.
    """

    def __init__(self, name, pre, add, delete, is_noop=False):
        """
        Constructor
        """
        self.pre = pre  # list of the precondition propositions
        self.add = add  # list of the propositions that will be added after applying the action
        self.delete = delete  # list of the propositions that will be deleted after applying the action
        self.name = name  # the name of the action as string
        self.noOp = is_noop  # true if the action is a noOp

    def get_pre(self):
        return self.pre

    def get_add(self):
        return self.add

    def get_delete(self):
        return self.delete

    def get_name(self):
        return self.name

    def is_pre_cond(self, prop):
        return prop in self.pre

    def is_pos_effect(self, prop):
        """
        True if the proposition prop is a positive effect of the action
        """
        return prop in self.add

    def is_neg_effect(self, prop):
        """
        Returns true if the proposition prop is a negative effect of the action
        """
        return prop in self.delete

    def all_preconds_in_list(self, propositions):
        """
        Returns true if all the precondition of the action
        are in the propositions list / set
        propositions must be iterable
        """
        for pre in self.pre:
            if pre not in propositions:
                return False
        return True

    def is_noop(self):
        """
        Returns true if the action in noOp action
        """
        return self.noOp

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.name == other.name)

    def __str__(self):
        return self.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)
