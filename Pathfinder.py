'''
The Pathfinder class is responsible for finding a solution (i.e., a
sequence of actions) that takes the agent from the initial state to all
of the goals with optimal cost.

This task is done in the solve method, as parameterized
by a maze pathfinding problem, and is aided by the SearchTreeNode DS.
'''

from MazeProblem import MazeProblem
from SearchTreeNode import SearchTreeNode
import unittest
from queue import PriorityQueue
import math
import itertools
from itertools import tee

def heuristic(curr, goal):
    return math.sqrt((curr[0] - goal[0])**2 + (curr[1] - goal[1])**2)

def asearch(problem, initial, goal):
    start = SearchTreeNode(initial, None, None, 0, heuristic(initial, goal))
    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()
    while not frontier.empty():
        current = frontier.get()
        if current.state == goal:
            return (current.totalCost, makePath(current))
        for action, cost, state in problem.transitions(current.state):
            if state not in explored:
                frontier.put(SearchTreeNode(state, action, current, current.totalCost + cost, heuristic(current.state, goal)))
        explored.add(current)
    return []

def solve (problem, initial, goals):
    paths = dict()
    best_cost = math.inf
    best_route = []
    nodes = goals.copy()
    nodes.insert(0, initial)
    #print(goals)
    permutations = list(itertools.permutations(range(len(nodes))))
    #print(permutations)
    for i in permutations:
        current_path = []
        current_cost = 0
        #print(i)
        pairs = list(pairwise(i))
        #print(pairs)
        for pair in pairs:
            #print(pair)
            x = pair[0]
            y = pair[1]
            path = asearch(problem, nodes[x], nodes[y])
            paths[pair] = (path[0], path[1])
            current_cost += path[0]
            current_path.extend(path[1])
            #print(current_path)
            #print(current_cost)
        if (current_cost < best_cost):
            best_cost = current_cost
            #print(best_cost)
            best_route = current_path
            print(best_route)
    return best_route


def makePath(goalNode):
    path = []
    node = goalNode
    while node.parent:
        path.append(node.action)
        node = node.parent
    return list(reversed(path))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class PathfinderTests(unittest.TestCase):

    def test_maze1(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.M.X",
                "X.X.X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (1, 3)
        goals   = [(5, 3)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 8)

    def test_maze2(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.M.X",
                "X.X.X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (1, 3)
        goals   = [(3, 3),(5, 3)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 12)

    def test_maze3(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.MMX",
                "X...M.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (5, 1)
        goals   = [(5, 3), (1, 3), (1, 1)]
        soln = solve(problem, initial, goals)
        print(soln)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 12)

    def test_maze4(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.XXX",
                "X...X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (5, 1)
        goals   = [(5, 3), (1, 3), (1, 1)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln == None)

if __name__ == '__main__':
    unittest.main()
