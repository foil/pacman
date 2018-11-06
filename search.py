# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    def _dfs(state):
        if problem.isGoalState(state):
            return True
    
        visited.add(state)
        successors = problem.getSuccessors(state)
        for nextState, action, cost in successors:
            if nextState not in visited:
                actions.append(action)
                res = _dfs(nextState)
                if res:
                    return True
                actions.pop()
    
        return False

    actions = []
    visited = set()
    _dfs(problem.getStartState())
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    cur_state = problem.getStartState()
    states = util.Queue()
    states.push(cur_state)
    visited = dict()
    visited[cur_state] = (None, None)
    found = False
    actions = []

    while not states.isEmpty():
        cur_state = states.pop()
        if problem.isGoalState(cur_state):
            found = True
            break

        successors = problem.getSuccessors(cur_state)
        for next_state, action, cost in successors:
            if next_state not in visited: 
                visited[next_state] = (cur_state, action)
                states.push(next_state)

    if not found:
        return actions

    while cur_state is not None:
        cur_state, action = visited[cur_state]
        if action is not None:
            actions.insert(0, action)

    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    stack = util.Stack()
    stack.push((state, 0))
    visited = dict()
    visited[state] = (None, None)
    found = False
    actions = []

    while not stack.isEmpty():
        state, total_cost = stack.pop()
        if problem.isGoalState(state):
            found = True
            break

        successors = problem.getSuccessors(state)
        for next_state, action, cost in successors:
            if next_state not in visited or problem.isGoalState(next_state):
                visited[next_state] = (state, action)
                stack.push((next_state, total_cost + cost))

        stack.list.sort(key=lambda tup: tup[1], reverse=True)

    if not found:
        return actions

    while state is not None:
        state, action = visited[state]
        if action is not None:
            actions.insert(0, action)

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    open_list = util.PriorityQueue()
    open_list.push((start_state, [], 0), 0) # (state, actions, total_cost), F
    close_list = []

    while not open_list.isEmpty():
        state, actions, total_cost = open_list.pop()
        if problem.isGoalState(state):
            return actions

        close_list.append(state)
        successors = problem.getSuccessors(state)
        for next_state, action, cost in successors:
            if next_state not in close_list or problem.isGoalState(next_state):
                close_list.append(next_state)
                next_actions = actions[:]
                next_actions.append(action)
                next_total_cost = total_cost + cost
                F = next_total_cost + heuristic(next_state, problem)

                for index, (f, c, (open_state, _, open_cost)) in enumerate(open_list.heap):
                    if open_state == next_state:
                        if open_cost <= next_total_cost:
                            break
                        del open_list.heap[index]
                        open_list.push((next_state, next_actions, next_total_cost), F)
                        open_list.count -= 1
                        break
                else:
                    open_list.push((next_state, next_actions, next_total_cost), F)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
