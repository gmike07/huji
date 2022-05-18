"""
In search.py, you will implement generic search algorithms
"""

import util

class Node:
    def __init__(self, state, prev=None, action=None, g_cost=0):
        self.state = state
        self.prev = prev
        self.action = action
        self.g_cost = g_cost

    def reconstruct_path(self):
        path = []
        current = self
        while current.prev is not None:
            path.append(current.action)
            current = current.prev
        return path[::-1]


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def reconstruct_path(current, path_mapping):
    path = []
    while current in path_mapping and path_mapping[current] != None:
        previous, action = path_mapping[current]
        path.append(action)
        current = previous
    return path[::-1]


def generic_graph_search(fringe, problem):
    start_node = Node(problem.get_start_state())
    closed = set()
    fringe.push(start_node)
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return current.reconstruct_path()
        if current.state not in closed:
            closed.add(current.state)
            for successor, action, stepCost in problem.get_successors(current.state):
                fringe.push(Node(successor, current, action, current.g_cost + stepCost))
    raise Exception("no solution exists in this problem")


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return generic_graph_search(util.Stack(), problem)


    fringe = util.Stack()
    closed = set()
    start_state = problem.get_start_state()
    fringe.push(start_state)
    path_mapping = {start_state: None}
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return reconstruct_path(current, path_mapping)
        if current.state not in closed:
            closed |= {current.state}
            for successor, action, stepCost in problem.get_successors(current.state):
                if successor not in path_mapping:
                    fringe.push(successor)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return generic_graph_search(util.Queue(), problem)


    fringe = util.Queue()
    closed = set()
    start_state = problem.get_start_state()
    fringe.push(start_state)
    path_mapping = {start_state: None}
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current):
            return reconstruct_path(current, path_mapping)
        if current not in closed:
            closed |= {current}
            for successor, action, stepCost in problem.get_successors(current):
                if successor not in path_mapping:
                    fringe.push(successor)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return generic_graph_search(util.PriorityQueueWithFunction(lambda node: node.g_cost), problem)


    start_state = problem.get_start_state()
    g_function = {start_state: 0}
    fringe = util.PriorityQueue()
    closed = set()
    fringe.push(start_state, 0)
    path_mapping = {start_state: None}
    while not fringe.isEmpty():
        current = fringe.pop()
        # print(g_function[current])
        if problem.is_goal_state(current):
            return reconstruct_path(current, path_mapping)
        if current not in closed:
            closed |= {current}
            for successor, action, stepCost in problem.get_successors(current):
                dist = g_function[current] + stepCost
                if successor not in path_mapping or dist < g_function[successor]:
                    g_function[successor] = dist
                    fringe.push(successor, dist)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")

    start_state = problem.get_start_state()
    vertex = Vertex(start_state, 0)
    fringe = util.PriorityQueueWithFunction(lambda x: x.f_cost)
    closed = set()
    fringe.push(vertex)
    path_mapping = {}
    while not fringe.isEmpty():
        current = fringe.pop()
        print(current.f_cost)
        state = current.state
        if problem.is_goal_state(state):
            return reconstruct_path(state, path_mapping)
        if state not in closed:
            closed |= {state}
            for successor, action, stepCost in problem.get_successors(state):
                if successor not in closed:
                    g_cost = current.g_cost + stepCost
                    fringe.push(Vertex(successor, g_cost))
                    path_mapping[successor] = (state, action)

    raise Exception("no solution exists in this problem")


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    return generic_graph_search(util.PriorityQueueWithFunction(lambda node: node.g_cost + heuristic(node.state, problem)), problem)


    start_node = Node(problem.get_start_state())
    f_function = lambda node: node.g_cost + heuristic(node.state, problem)
    fringe = util.PriorityQueueWithFunction(f_function)
    closed = set()
    fringe.push(start_node)
    while not fringe.isEmpty():
        current = fringe.pop()
        print(f_function(current))
        if problem.is_goal_state(current.state):
            return current.reconstruct_path()
        if current.state not in closed:
            closed.add(current.state)
            for successor, action, stepCost in problem.get_successors(current.state):
                fringe.push(Node(successor, current, action, current.g_cost + stepCost))
    raise Exception("no solution exists in this problem")

    #try
    import time
    t = time.time()
    start_state = problem.get_start_state()
    g_function = {start_state: 0}
    f_function = lambda x: g_function[x] +  heuristic(x, problem)
    fringe = util.PriorityQueueWithFunction(f_function)
    closed = set()
    fringe.push(start_state)
    path_mapping = {start_state: None}
    while not fringe.isEmpty():
        current = fringe.pop()
        print(f_function(current))
        if problem.is_goal_state(current):
            a = reconstruct_path(current, path_mapping)
            print(time.time() - t)
            return a
        if current not in closed:
            closed |= {current}
            for successor, action, stepCost in problem.get_successors(current):
                dist = g_function[current] + stepCost
                if successor not in path_mapping or dist < g_function[successor]:
                    g_function[successor] = dist
                    fringe.push(successor)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")


    start_state = problem.get_start_state()
    h_cost = heuristic(start_state, problem)
    vertex = Vertex(start_state, 0, h_cost)
    fringe = util.PriorityQueueWithFunction(lambda x: x.f_cost)
    closed = set()
    fringe.push(vertex)
    path_mapping = {}
    while not fringe.isEmpty():
        current = fringe.pop()
        print(current.f_cost)
        state = current.state
        if problem.is_goal_state(state):
            return reconstruct_path(state, path_mapping)
        if state not in closed:
            closed |= {state}
            for successor, action, stepCost in problem.get_successors(state):
                if successor not in closed:
                    g_cost = current.g_cost + stepCost
                    h_cost = heuristic(successor, problem)
                    fringe.push(Vertex(successor, g_cost, h_cost))
                    path_mapping[successor] = (state, action)

    raise Exception("no solution exists in this problem")
    #end try

    start_state = problem.get_start_state()
    g_function = {start_state: 0}
    h_function = {start_state: heuristic(start_state, problem)}
    f_function = lambda x: g_function[x] + h_function[x]
    fringe = util.PriorityQueueWithFunction(f_function)
    closed = set()
    fringe.push(start_state)
    path_mapping = {}
    while not fringe.isEmpty():
        current = fringe.pop()
        # print(f_function(current))
        if problem.is_goal_state(current):
            a= reconstruct_path(current, path_mapping)
            print(time.time()-t)
            return a
        if current not in closed:
            closed |= {current}
            for successor, action, stepCost in problem.get_successors(current):
                if successor not in closed:
                    g_function[successor] = g_function[current] + stepCost
                    h_function[successor] = heuristic(successor, problem)
                    fringe.push(successor)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")

def greedy_best_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    #try
    return generic_graph_search(util.PriorityQueueWithFunction(lambda node: heuristic(node.state, problem)), problem)


    start_state = problem.get_start_state()
    h_helper = lambda x: heuristic(x, problem)
    fringe = util.PriorityQueueWithFunction(h_helper)
    closed = set()
    fringe.push(start_state)
    path_mapping = {start_state: None}
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current):
            return reconstruct_path(current, path_mapping)
        if current not in closed:
            closed |= {current}
            for successor, action, stepCost in problem.get_successors(current):
                if successor not in path_mapping:
                    fringe.push(successor)
                    path_mapping[successor] = (current, action)

    raise Exception("no solution exists in this problem")

def a_star_search_banned(problem, invalid_set, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    start_node = Node(problem.get_start_state())
    f_function = lambda node: node.g_cost + heuristic(node.state, problem)
    fringe = util.PriorityQueueWithFunction(f_function)
    closed = set()
    fringe.push(start_node)
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current.state) and current.state not in invalid_set:
            return current.reconstruct_path()
        if current.state not in closed:
            closed.add(current.state)
            for successor, action, stepCost in problem.get_successors(
                    current.state):
                fringe.push(Node(successor, current, action,
                                 current.g_cost + stepCost))
    return None

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
