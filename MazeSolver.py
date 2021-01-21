import math
from simpleai.search import SearchProblem, astar


# This codebase was inspired from one of the tutorials
# As I did the tutorial myself and the purpose was learning
# I consider this to be my code, but it is inspired from
# what I have been taught and tasked to do during the CET313 tutorials
# Author: Emanuel Iulian Gheoghe
# Project: A*GO - Professional Pracice Week 2
# Module: CET313

class MazeSolver(SearchProblem):

    # this function is initializing the grid (board) and the variables
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        self.initial = (0, 7)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)
        super(MazeSolver, self).__init__(initial_state=self.initial)

    # this function is defining the method that takes actions
    # to arrive at the solution
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    # updating state based on action
    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)

        return new_state

    # Checking if the goal has been reached
    def is_goal(self, state):
        return state == self.goal

    # computing cost of taking an action
    def cost(self, state, action, state2):
        return COSTS[action]

    # heuristic that is used to arrive at the solution
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal

        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


if __name__ == "__main__":
    f = open("maze-map.txt", "r")
    # define map
    MAP = f.read()
    f.close()
    print(MAP)  # print map for debug purposes
    MAP = [list(x) for x in MAP.split("\n") if x]

    # defining cost of moving around the map
    cost_regular = 1.0
    cost_diagonal = 1.7

    # Cost dictionary
    COSTS = {
        "up": cost_regular,
        "down": cost_regular,
        "left": cost_regular,
        "right": cost_regular,
        "up left": cost_regular,
        "up right": cost_regular,
        "down left": cost_regular,
        "down right": cost_regular,
    }
    # creating maze solver object
    problem = MazeSolver(MAP)

    # running solver
    result = astar(problem, graph_search=True)

    # extracting the path
    path = [x[1] for x in result.path()]

    # output file for the resulted path
    r = open("path-coord.txt", "w")
    # print result for debug purposes
    print()
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print('o', end='')
            elif (x, y) == problem.goal:
                print('x', end='')
            elif (x, y) in path:
                print('-', end='')
                coords = str(y) + "," + str(x) + "\n"
                coords.replace('(', '')
                coords.replace(")", "")
                r.write(coords)
            else:
                print(MAP[y][x], end='')
        print()
