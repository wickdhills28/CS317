# Steven Nguyen stn812 11213790

from random import randint
from CS317A3 import A1Search as A1Search
import time


class Problem:
    # problem is an array with the the target being at index 0 and the rest being the numbers
    def __init__(self, filename, testing=False, problem_num = 0):
        self.all_problems = self.read_file(filename)
        if testing:
            self.problem = self.all_problems[problem_num]
        else:
            random_int = randint(0, len(self.all_problems) - 1)
            self.problem = self.all_problems[random_int]



    def initial_state(self):
        return State(self.problem)

    # Takes in a row/col as a list and makes sure that every elements occurs only once
    def all_diff(self,int_list):
        for i in int_list:
            if int_list.count(i) > 1:
                return False
        return True

    # Swap the rows and columns to check if all_diff()
    def row_col_swap(self, state):
        current_state = state.cur_state
        col_state = [] # Swap the rows and columns

        for i in range(len(current_state)):
            col_state.append([])

        for row in current_state:
            for i in range(len(row)):
                col_state[i].append(row[i])

        return col_state

    def is_goal(self, state):
        current_state = state.cur_state
        # Check rows
        for row in current_state:
            # First check for unassigned values
            if 0 in row:
                return False
            if self.all_diff(row):
                return False

        # Check columns
        for row in self.row_col_swap(state):
            if 0 in row:
                return False

            if not self.all_diff(row):
                return False

        return True

    # Actions can be integers from 1->N
    def actions(self, state):

        action_list = []

        for i in range(len(state.cur_state)):
            action_list.append(i)

        return action_list

    # Fills in the first blank
    def result(self, state, action):
        if len(state.blank_locations()) == 0:
            return State(state.cur_state)
        first_blank = state.blank_locations()[0]
        row = first_blank[0]
        col = first_blank[1]

        state.cur_state[row][col] = action

        return State(state.cur_state)


    # Read in a file containing example sets
    def read_file(self,filename):
        all_problems = []
        with open(filename) as f:
            data = f.readlines()

            total_problems = int(data[0])
            for i in range(total_problems):
                all_problems.append([])

            cur_line = 1
            num_lines = int(data[cur_line])
            stop_read = cur_line + num_lines + 1

            for i in range(total_problems):
                num_lines = int(data[cur_line])
                stop_read = cur_line + num_lines + 1
                for j in range(cur_line, stop_read):
                    sub_list = [words for segments in data[j] for words in segments.split()]

                    all_problems[i].append(sub_list)
                cur_line = stop_read + 1

            for sub_list in all_problems:
                sub_list.pop(0)

            for example in all_problems:
                for row in example:
                    for i in range(len(row)):
                        if row[i] == "_":
                            row[i] = 0
                        else:
                            row[i] = int(row[i])
        return all_problems


class State:
    def __init__(self, astate):
        self.cur_state = astate

    # Gives a list of blank locations where each elements is a tuple (row,col)
    def blank_locations(self):
        locations = []
        N = len(self.cur_state)

        if N == 0:
            return None

        for row in range(N):
            for col in range(N):
                if self.cur_state[row][col] == 0:
                    locations.append((row,col))

        return locations


if __name__ == "__main__":
    print("TESTING ASAP")
    start1 = time.time()
    prob_obj = Problem("LatinSquares.txt", True,1)
    p = prob_obj.problem
    search = A1Search.Search(prob_obj)
    result = search.DepthFirstSearch(prob_obj.initial_state())
    oneresult1 = time.time()-start1
    print(oneresult1)
    #
    start2 = time.time()
    prob_obj = Problem("LatinSquares.txt", True,5)
    p = prob_obj.problem
    search = A1Search.Search(prob_obj)
    result = search.DepthFirstSearch(prob_obj.initial_state())
    tworesult2 = time.time()-start2
    print(tworesult2)

    print(tworesult2/oneresult1)
    #
    # start3 = time.time()
    # prob_obj = Problem("LatinSquares.txt", True,6)
    # p = prob_obj.problem
    # search = A1Search.Search(prob_obj)
    # result = search.DepthFirstSearch(prob_obj.initial_state())
    # threeresult3 = time.time()-start3
    #
    # print((oneresult1+ tworesult2+ threeresult3)/3)
    #
    # print((0.04515401522318522/0.04373764991760254)*100)







































