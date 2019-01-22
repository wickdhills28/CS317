# CMPT 317.201809: A Python implementation of node queues for uninformed search.
# Assumes a problem class with the methods:
#   is_goal(problem_state): returns True if the state is the goal state
#   actions(problem_state): returns a list of all valid actions in state
#                           (the actions are only passed to result())
#   result(state, action): returns a new state that is the result of doing action in state.
#
# Search methods are based on TreeSearch (no repeated state checking):
# 1. DepthFirstSearch(s)
# 2. BreadthFirstSearch(s)
# 3. DepthLimitedSearch(s, dlimit)
# 4. IDS(s)
# These methods return a SearchResult object, containing information about the search.  See the definition below.
#
# Usage:
#   import UninformedSearch as Search
#   pi = <create a problem instance>
#   searcher = Search.Search(pi, <timelimit>)
#   s = <create an initial state for the problem>
#   result = searcher.DepthFirstSearch(s)
#            # or any of the methods above
#   print(str(result))
#   # or public access to any of the data stored in the result.

import time as time
from CS317A3 import Frontier as Frontiers


class SearchNode(object):
    """A data structure to store search information"""

    def __init__(self, state, parent_node, step_cost=1):
        """A Node stores
             a single Problem state,
             a parent node
             the new node's depth
             the new node's path cost
        """
        self.state = state
        self.parent = parent_node
        if parent_node is None:
            self.path_cost = 0
            self.depth = 0
        else:
            self.path_cost = parent_node.path_cost + step_cost
            self.depth = parent_node.depth + 1

    def __str__(self):
        return '<' + str(self.depth) + '> ' + str(self.state) + ' (' + str(self.path_cost) + ')'

    def display_steps(self):
        def disp(node):
            if node.parent is not None:
                disp(node.parent)
                print(str(node.state))

        print("Solution:")
        disp(self)


class SearchResult(object):
    """A data structure to return information about how the search turned out."""

    def __init__(self, success=False, result=None, time=0, nodes=0, space=0, cutoff=False):
        self.success = success  # Boolean: did search find a solution?
        self.result = result    # SearchNode: a node containing a goal state, or None if no solution found
        self.time = time        # float: how much time was spent searching?  Not really accurate, but good enough for fun
        self.nodes = nodes      # integer: How many nodes were expaded during the search?
        self.space = space      # integer: What was the maximum size of the frontier during search?
        self.cutoff = cutoff    # Boolean: For IDS, did the depth limited search reach the depth limit before failing?

    def __str__(self):
        """Make a nice mess"""
        text = ''
        if self.success:
            text += 'Search successful'
        else:
            text += 'Search failed'
        text += ' (' + str(self.time) + ' sec, ' + str(self.nodes) + ' nodes, ' + str(self.space) + ' queue)'
        return text


class Search(object):
    """A class to contain uninformed search algorithms.
       API users should call the public methods.
       Subclasses inheriting this class can call _treeSearch() or _dltree_search()
    """

    def __init__(self, problem, timelimit=10):
        """The Search object needs to be given:
            the search Problem,
            a queue to store Node(s) to explore
            possibly a depth limit to terminate search
        """
        self._problem = problem
        self._frontier = None
        self._time_limit = timelimit

    def __childNode(self, parent_node, action):
        """take the parent node, and an action, and produce the new state"""

        child = self._problem.result(parent_node.state, action)
        return SearchNode(child, parent_node)

    def _tree_search(self, initial_state):
        """Search through the State space starting from an initial State.
           Simple tree search algorithm.
           Monitors:
                time so as not to exceed a time limit.
                number of nodes expanded
                size of the frontier at any point
        """

        start_time = time.time()
        now = start_time
        self._frontier.add(SearchNode(initial_state, None))
        node_counter = 0
        max_space = 0

        while not self._frontier.is_empty() and now - start_time < self._time_limit:
            max_space = max(max_space, len(self._frontier))
            this_node = self._frontier.remove()
            node_counter += 1
            now = time.time()
            if self._problem.is_goal(this_node.state):
                return SearchResult(success=True, result=this_node,
                                    nodes=node_counter, space=max_space, time=now - start_time)
            else:
                for act in self._problem.actions(this_node.state):
                    self._frontier.add(self.__childNode(this_node, act))

        # empty frontier implies no solution
        now = time.time()
        return SearchResult(success=False, result=None,
                            nodes=node_counter, space=max_space, time=now - start_time)


    def DepthFirstSearch(self, initial_state):
        """
        Perform depth-first search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :return: SearchResult
        """
        # configure search
        self._frontier = Frontiers.FrontierLIFO()
        # run search
        return self._tree_search(initial_state)

    def BreadthFirstSearch(self, initial_state):
        """
        Perform breadth-first search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :return: SearchResult
        """
        # configure search
        self._frontier = Frontiers.FrontierFIFO()
        # run search
        return self._tree_search(initial_state)

    def DepthLimitedSearch(self, initial_state, limit):
        """
        Perform depth-limited search of the problem,
        starting at a given initial state.
        :param initial_state: a Problem State
        :param limit: the maximum allowable depth
        :return: SearchResult
        """
        # configure search
        self._frontier = Frontiers.FrontierLIFO_DL(limit)
        # run search
        result = self._tree_search(initial_state)
        result.cutoff = self._frontier._cutoff
        return result

    def IDS(self, initial_state):
        """Iterative deepening Search successively increases the search depth
           the search depth until a solution is found."""
        limit = 0
        nodes = 0
        time = 0
        space = 0
        while time < self._time_limit:
            answer = self.DepthLimitedSearch(initial_state, limit)
            if answer.success:
                answer.time += time
                answer.nodes += nodes
                answer.space = max(answer.space, space)
                return answer
            elif not self._frontier._cutoff:
                return SearchResult(success=False, result=None, nodes=nodes, space=space, time=time)
            else:
                nodes += answer.nodes
                time += answer.time
                limit += 1
                space = max(answer.space, space)

        return SearchResult(success=False, result=None, nodes=nodes, space=space, time=time)
