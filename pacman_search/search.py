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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = []
    stack = util.Stack()
    #Each item in the stack holds a state and a list of Directions to get there
    stack.push((problem.getStartState(),[]))
    while stack:
        curr, path = stack.pop()
        if problem.isGoalState(curr):
            return path
        if curr not in visited:
            adj = problem.getSuccessors(curr)
            for i in adj:
                #Update the path with the next direction
                new_path = path + [i[1]]
                #Add each discovered node to the stack
                stack.push((i[0],new_path))
        visited.append(curr)
    raise Exception("No path was found to the goal") 

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #This is identical to DFS except with a queue insted of a stack
    visited = []
    queue = util.Queue()
    queue.push((problem.getStartState(),[]))
    while queue:
        curr, path = queue.pop()
        if problem.isGoalState(curr):
            return path
        if curr not in visited:
            adj = problem.getSuccessors(curr)
            for i in adj:
                new_path = path + [i[1]]
                queue.push((i[0],new_path))
        visited.append(curr)
    raise Exception("No path was found to the goal") 


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    #Using a priority queue with the actual cost as the priority function
    pQueue = util.PriorityQueue()
    #Cost of start node is 0, also store the past_cost in the queue
    pQueue.push((problem.getStartState(),[], 0),0)
    while pQueue:
        #Get past cost as well as node and path
        curr, path, past_cost = pQueue.pop()
        if problem.isGoalState(curr):
            return path
        if curr not in visited:
            adj = problem.getSuccessors(curr)
            for next_state,direction,weight in adj:
                new_path = path + [direction]
                #Getting the cost of visiting the next node
                cost = past_cost + weight
                pQueue.push((next_state,new_path,cost), cost)
        visited.append(curr)
    raise Exception("No path was found to the goal") 



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    #Using a priority queue with the cost as the priority function
    pQueue = util.PriorityQueue()
    start = problem.getStartState()
    #Store past_cost, but use the sum of past_cost and heuristic as the priorirty function
    pQueue.push((problem.getStartState(),[], 0),heuristic(start,problem))
    while pQueue:
        curr, path, past_cost = pQueue.pop()
        if problem.isGoalState(curr):
            return path
        if curr not in visited:
            adj = problem.getSuccessors(curr)
            for node,direction,weight in adj:
                n_path = path + [direction]
                #Calculate actual cost and store in the node but use actual cost + heuristic as priority function
                actual_cost = past_cost + weight
                f_cost = actual_cost + heuristic(node, problem)
                pQueue.push((node,n_path,actual_cost), f_cost)
        visited.append(curr)
    raise Exception("No path was found to the goal") 



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
