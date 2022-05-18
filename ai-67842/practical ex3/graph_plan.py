from util import Pair
from proposition_layer import PropositionLayer
from plan_graph_level import PlanGraphLevel
from action import Action
from pgparser import PgParser


class GraphPlan(object):
    """
    A class for initializing and running the graphplan algorithm
    """

    def __init__(self, _domain, _problem):
        """
        Constructor
        """
        self.independent_actions = set()
        self.no_goods = []
        self.graph = []
        p = PgParser(_domain, _problem)
        self.actions, self.propositions = p.parse_actions_and_propositions()
        # list of all the actions and list of all the propositions

        self.initial_state, self.goal = p.parse_problem()
        # the initial state and the goal state are lists of propositions

        self.create_noops()
        # creates noOps that are used to propagate existing propositions from one layer to the next

        self.independent()
        # creates independent actions set and updates self.independent_actions
        PlanGraphLevel.set_independent_actions(self.independent_actions)
        PlanGraphLevel.set_actions(self.actions)
        PlanGraphLevel.set_props(self.propositions)

    def graph_plan(self):
        """
        The graphplan algorithm.
        The code calls the extract function which you should complete below
        """
        # initialization
        init_state = self.initial_state
        level = 0
        self.no_goods = []  # make sure you update noGoods in your backward search!
        self.no_goods.append([])
        # create first layer of the graph, note it only has a proposition layer which consists of the initial state.
        prop_layer_init = PropositionLayer()
        for prop in init_state:
            prop_layer_init.add_proposition(prop)
        pg_init = PlanGraphLevel()
        pg_init.set_proposition_layer(prop_layer_init)
        self.graph.append(pg_init)
        size_no_good = -1

        """
        While the layer does not contain all of the propositions in the goal state,
        or some of these propositions are mutex in the layer we,
        and we have not reached the fixed point, continue expanding the graph
        """

        while self.goal_state_not_in_prop_layer(self.graph[level].get_proposition_layer().get_propositions()) or \
                self.goal_state_has_mutex(self.graph[level].get_proposition_layer()):
            if self.is_fixed(level):
                return None
                # this means we stopped the while loop above because we reached a fixed point in the graph.
                #  nothing more to do, we failed!

            self.no_goods.append([])
            level = level + 1
            pg_next = PlanGraphLevel()  # create new PlanGraph object
            pg_next.expand(
                self.graph[level - 1])  # calls the expand function, which you are implementing in the PlanGraph class
            self.graph.append(pg_next)  # appending the new level to the plan graph

            size_no_good = len(self.no_goods[level])  # remember size of nogood table

        plan_solution = self.extract(self.graph, self.goal, level)
        # try to extract a plan since all of the goal propositions are in current graph level, and are not mutex

        while plan_solution is None:  # while we didn't extract a plan successfully
            level = level + 1
            self.no_goods.append([])
            pg_next = PlanGraphLevel()  # create next level of the graph by expanding
            pg_next.expand(self.graph[level - 1])  # create next level of the graph by expanding
            self.graph.append(pg_next)
            plan_solution = self.extract(self.graph, self.goal, level)  # try to extract a plan again
            if plan_solution is None and self.is_fixed(level):  # if failed and reached fixed point
                if len(self.no_goods[level - 1]) == len(self.no_goods[level]):
                    # if size of nogood didn't change, means there's nothing more to do. We failed.
                    return None
                size_no_good = len(self.no_goods[level])  # we didn't fail yet! update size of no good
        return plan_solution

    def extract(self, graph, sub_goals, level):
        """
        The backsearch part of graphplan that tries
        to extract a plan when all goal propositions exist in a graph plan level.
        """

        if level == 0:
            return []
        if sub_goals in self.no_goods[level]:
            return None
        plan_solution = self.gp_search(graph, sub_goals, [], level)
        if plan_solution is not None:
            return plan_solution
        self.no_goods[level].append([sub_goals])
        return None

    def gp_search(self, graph, sub_goals, _plan, level):
        if len(sub_goals) == 0:
            new_goals = []
            for action in _plan:
                for prop in action.get_pre():
                    if prop not in new_goals:
                        new_goals.append(prop)
            new_plan = self.extract(graph, new_goals, level - 1)
            if new_plan is None:
                return None
            else:
                return new_plan + _plan

        prop = sub_goals[0]
        providers = []
        for action1 in [act for act in graph[level].get_action_layer().get_actions() if prop in act.get_add()]:
            no_mutex = True
            for action2 in _plan:
                if Pair(action1, action2) not in self.independent_actions:
                    no_mutex = False
                    break
            if no_mutex:
                providers.append(action1)
        for action in providers:
            new_sub_goals = [g for g in sub_goals if g not in action.get_add()]
            plan_clone = list(_plan)
            plan_clone.append(action)
            new_plan = self.gp_search(graph, new_sub_goals, plan_clone, level)
            if new_plan is not None:
                return new_plan
        return None

    def goal_state_not_in_prop_layer(self, propositions):
        """
        Helper function that receives a  list of propositions (propositions) and returns true
        if not all the goal propositions are in that list
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def goal_state_has_mutex(self, prop_layer):
        """
        Helper function that checks whether all goal propositions are non mutex at the current graph level
        """
        for goal1 in self.goal:
            for goal2 in self.goal:
                if prop_layer.is_mutex(goal1, goal2):
                    return True
        return False

    def is_fixed(self, level):
        """
        Checks if we have reached a fixed point, i.e. each level we'll expand would be the same,
        thus no point in continuing
        """
        if level == 0:
            return False

        if len(self.graph[level].get_proposition_layer().get_propositions()) == \
                len(self.graph[level - 1].get_proposition_layer().get_propositions()) and \
                len(self.graph[level].get_proposition_layer().get_mutex_props()) == \
                len(self.graph[level - 1].get_proposition_layer().get_mutex_props()):
            return True
        return False

    def create_noops(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name, precon, add, delete, True)
            self.actions.append(act)
            prop.add_producer(act)

    def independent(self):
        """
        Creates a set of independent actions
        """
        for i in range(len(self.actions)):
            for j in range(i + 1, len(self.actions)):
                act1 = self.actions[i]
                act2 = self.actions[j]
                if independent_pair(act1, act2):
                    self.independent_actions.add(Pair(act1, act2))

    def is_independent(self, a1, a2):
        return Pair(a1, a2) in self.independent_actions

    @staticmethod
    def no_mutex_action_in_plan(plan_, act, action_layer):
        """
        Helper action that you may want to use when extracting plans,
        returns true if there are no mutex actions in the plan
        """
        for plan_act in plan_:
            if action_layer.is_mutex(Pair(plan_act, act)):
                return False
        return True


def independent_pair(a1, a2):
    """
    Returns true if the actions are neither have inconsistent effects
    nor they interfere one with the other.
    You might want to use those functions:
    a1.get_pre() returns the pre list of a1
    a1.get_add() returns the add list of a1
    a1.get_delete() return the del list of a1
    a1.is_pre_cond(p) returns true is p is in a1.get_add()
    a1.is_pos_effect(p) returns true is p is in a1.get_add()
    a1.is_neg_effect(p) returns true is p is in a1.get_delete()
    """
    pre1, del1, add1 = set(a1.get_pre()), set(a1.get_delete()), set(a1.get_add())
    pre2, del2, add2 = set(a2.get_pre()), set(a2.get_delete()), set(a2.get_add())

    # inconsistent effects
    if (del1 & add2) or (del2 & add1):
        return False

    # interfere one with the other
    if (del1 & pre2) or (del2 & pre1):
        return False

    return True


if __name__ == '__main__':
    import sys
    import time

    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print("Usage: graph_plan.py domain_name problem_name")
        exit()
    domain = 'dwrDomain.txt'
    problem = 'dwrProblem.txt'
    if len(sys.argv) == 3:
        domain = str(sys.argv[1])
        problem = str(sys.argv[2])

    gp = GraphPlan(domain, problem)
    start = time.clock()
    plan = gp.graph_plan()
    elapsed = time.clock() - start
    if plan is not None:
        print("Plan found with %d actions in %.2f seconds" % (len([act for act in plan if not act.is_noop()]), elapsed))
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
