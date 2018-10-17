# searchAgents.py
# ---------------
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
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=dfs

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"
"""

import time
import copy

import searchFunctions
from game import Agent
from game import Directions
from searchProblems import *

UNREACHABLE_GOAL_STATE = [Directions.STOP]


class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
    or location specified in the map

    Options for fn include:
      dfs
      bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(searchFunctions):
            raise AttributeError, fn + ' is not a search function in searchProblems.py.'
        func = getattr(searchFunctions, fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(searchFunctions):
                heur = getattr(searchFunctions, heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or searchProblems.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys():
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        other_params = {}
        if len(state.data.layout.goals) > 0:
            other_params['goal'] = state.data.layout.goals[0]

        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        self.problem = self.searchType(state, **other_params)  # Makes a new search problem
        self.actions = self.searchFunction(self.problem)  # Find a path

        if self.actions == UNREACHABLE_GOAL_STATE:
            print "Unreachable goal state. Done!"
            self.reached_goal = True
            return

        self.reached_goal = reached_goal(self.actions, self.problem)
        totalCost = self.problem.getCostOfActions(self.actions)

        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if self.reached_goal:
            print "Reached goal state!. Done!"
        else:
            print "Failed to reach goal state, Exiting..."
        if '_expanded' in dir(self.problem): print('Search nodes expanded: %d' % self.problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            if self.reached_goal:
                state.data._win = True
            else:
                state.data._lose = True

            return Directions.STOP


def reached_goal(actions, problem):
    problem = copy.deepcopy(problem)

    try:
        problem.visualize = False
    except:
        pass

    current_state = problem.getStartState()
    for a in actions:
        possible_states = problem.getNextStates(current_state)
        for s in possible_states:
            if s[1] == a:
                current_state = s[0]
                break

    return problem.isGoalState(current_state)
