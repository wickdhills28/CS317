# Steven Nguyen stn812 11213790
from random import randint
from CS317A3 import A1Search as A1Search
import time


class Variable:
    def __init__(self, cur_val,identifier, given=True, dom=None):
        self.current_value = cur_val    # current_value of 0 means unassigned.
        self.domain = dom
        self.given = given  # Determines whether or not the value was given in the initial problem ***
        self.identifier = identifier # Identifier of a variable as a tuple of (row,col)
        # Set domain to an empty list when current value is not None
        if self.current_value is not None:
            self.domain = []

class State:

    def __init__(self, collection=None):
        self.cur_state = [] # EMPTY Collection of Variables
        self.changeable = [] # Contains tuples that indicate the location of changeable variables
        self.example = collection
        for i in range(len(self.example)):
            self.cur_state.append([])

        # Create collection of Variables each with empty domain
        for i in range(len(self.example)):
            for j in range(len(self.example)):
                # If value can be changed
                if self.example[i][j] == 0:
                    self.changeable.append((i, j))
                    new_var = Variable(self.example[i][j],(i,j),False)
                    self.set_up_domain(new_var)
                    self.cur_state[i].append(new_var)   # (i,j) will be the identifier
                else:
                    self.cur_state[i].append(Variable(self.example[i][j],(i,j)))   # Add Variable object with value to cur_state

    # Set up domain for input variable
    # Restricts the domains of Variable objects to values that do not appear in same row and col
    def set_up_domain(self, variable):

        # don't do this for any given variables
        if variable.given:
            return None

        domain = []
        given_example = self.example

        for i in range(1,len(self.cur_state)+1):
            domain.append(i)

        # Check constraints to get ALLOWABLE DOMAIN
        restricted = [] # Add all values in same row and column

        # Get location of variable
        row = variable.identifier[0]
        col = variable.identifier[1]

        # Get all values in same row and column
        for item in given_example[row]:
            restricted.append(item)   # TODO : Figure out why this is highlighted
        for a_row in given_example:
            restricted.append(a_row[col])
        for val in domain:
            if val in restricted:
                domain.remove(val) # Remove the integer from possible actions
        variable.domain = domain

        return "DOMAIN SET"


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

    # Takes in a a list of Variables and makes sure that every elements occurs only once
    def all_diff(self,alist):
        int_list = []

        # Grab the current value from each variable in the row/col
        for item in alist:
            int_list.append(item.current_value)

        for i in int_list:
            if int_list.count(i) > 1:
                return False
        return True

    # Swap the rows and columns to check if all_diff()
    def row_col_swap(self, state):
        current_state = state.cur_state.copy()
        col_state = [] # Swap the rows and columns

        for i in range(len(current_state)):
            col_state.append([])

        for row in current_state:
            for i in range(len(row)):
                col_state[i].append(row[i])

        return col_state

    def is_goal(self, state):
        #TODO : Double check that this is correct
        # NOTE: Any unassigned variables means INCOMPLETE and STOP CHECKING
        current_state = state.cur_state

        # Check rows
        for row in current_state:
            alist = []
            for item in row:
                alist.append(item.current_value)    # Grab the values of each variable to the list to check for repeats

            if 0 in alist:  # First check for unassigned value
                return False

            if not self.all_diff(alist):    # Check for repeats
                return False

        # Check columns
        for row in self.row_col_swap(state):
            alist = []
            for item in row:
                alist.append(item.current_value)    # Grab the values of each variable to the list to check for repeats

            if 0 in alist:  # First check for unassigned value
                return False

            if not self.all_diff(alist):    # Check for repeats
                return False

        return True

    # Gives a list of actions for a variable
    # Returns a tuple containg the list of actions and the variable identifier
    # Returns None if no possible actions ->  all variables assigned
    def actions(self, state):
        action_list = []
        current_state = state.cur_state
        altered_state = self.row_col_swap(state)    # REMINDER:  row_col_swap returns a 2-D List of Variables, NOT a state

        for i in range(1,len(state.cur_state)+1):
            action_list.append(i)

        # Check constraints to get ALLOWABLE DOMAIN
        for iden in state.changeable:
            row = iden[0]
            col = iden[1]

            var = current_state[row][col]
            if var.current_value == 0:  # Found first blank
                current_state[row][col].domain = action_list  # Set the domain of the variable to 1->N
                restricted = [] # Add all values in same row and column
                for item in current_state[row]:
                    restricted.append(item.current_value)
                for item2 in altered_state[col]:
                    restricted.append(item2.current_value)

                for val in action_list:
                    if val in restricted:
                        action_list.remove(val) # Remove the integer from possible actions

                identifier = (row,col)

                updated_action_list = []
                for action in action_list:
                    updated_action_list.append([identifier,action]) # Form of each element: [(row,col),value]

                return updated_action_list

        return [[(-1,-1),-1]] # Indicating that there are no more values


    # action -> tuple containing an identifer(as a tuple (row,col)) and a list of actions for that variable
    # ex. ((1,2), [1,3,6,7])
    def result(self, state, action):
        current_state = state.cur_state.copy()
        row = action[0][0]
        col = action[0][1]
        current_state[row][col].current_value = action[1]
        return State(current_state)

if __name__ == "__main__":
    print("TESTING ASAP")
    start1 = time.time()
    prob_obj = Problem("LatinSquares.txt", True,4)
    p = prob_obj.problem
    search = A1Search.Search(prob_obj)
    result = search.DepthFirstSearch(prob_obj.initial_state())
    oneresult1 = time.time()-start1

    start2 = time.time()
    prob_obj = Problem("LatinSquares.txt", True,5)
    p = prob_obj.problem
    search = A1Search.Search(prob_obj)
    result = search.DepthFirstSearch(prob_obj.initial_state())
    tworesult2 = time.time()-start2

    start3 = time.time()
    prob_obj = Problem("LatinSquares.txt", True,6)
    p = prob_obj.problem
    search = A1Search.Search(prob_obj)
    result = search.DepthFirstSearch(prob_obj.initial_state())
    threeresult3 = time.time()-start3

    print((oneresult1+ tworesult2+ threeresult3)/3)

    print((0.04515401522318522/0.04373764991760254)*100)



    # problem_num = 0
    # while problem_num<56:
    #     prob_obj = Problem("LatinSquares.txt", True,problem_num)
    #     p = prob_obj.problem
    #     # print("Q2 PROBLEM : "+str(p))
    #     search = A1Search.Search(prob_obj)
    #     result = search.DepthFirstSearch(prob_obj.initial_state())
    #     # print("Result : " + str(result))
    #     problem_num+=1

