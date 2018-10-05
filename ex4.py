# Class: CPSC 427-01
# Author: Jason Conci, Daniel Abrahms, Tyler Tiedt, Paul De Palma
# ID's:   -jconci      -dabrahms       -ttiedt      
# Assignment: Project 5 - Depth First Search
#
# INSTRUCTIONS FOR USE:
#   1. Should run in current state. When the machine finds the solution, it
#       will prompt the user, print the found solution, and state the number
#       of nodes checked before finding the solution. Enter 'True' as depth_first
#       parameter to view state_lst upon completion.
#
# Sources:
#   [1] An Eight-Puzzle Solver in Python
#          https://gist.github.com/flatline/8382021


from copy import deepcopy

#nested list representation of 8 puzzle. 0 is the blank
_init_state = [[2,8,3],
               [1,6,4],
               [7,0,5]]

# Nested list representation of our solved 8 puzzle, with 0 as the blank
_goal_state = [[1,2,3],
               [8,0,4],
               [7,6,5]]

# Our hard coded depth limit of 5
depth_limit = 5

# Our EightPuzzle object, which we create, and will be the controller for all that
# goes on in this program. Constructor initializes the game state equal to _init_state,
# and makes all stacks empty. See included methods for more details on implementation.
class EightPuzzle:
    closed = []
    opened = []
    depth = []
    def __init__(self):
        #child states will be kept in a list
        #the constructor adds the initial (i.e., parent state) to the list
        self.state_lst = [[row for row in _init_state]]
        self.closed = []
        self.opened = []
        self.depth = []

    #displays all states in the list
    def display(self):
        for state in self.state_lst:
            for row in state:
                print(row)
            print("")
    
    # Actual function which does the depth first search. Takes no parameters.
    # Implementation initializes opened, closed, and depth stacks, and loops.
    # While we have unopened nodes, we will pop them off the stack, and check
    # If they are our goal. If they are not, we check if we're at our depth
    # bound, and generate children based on whether or not we are at the depth
    # bound. Once we find our solution, we print to the user and return.
    #
    # NOTE: If you'd like to view the state_list upon finding solution, run the
    # function depth_first with parameter 'True'.
    #
    # NOTE: We've diverged slightly from the provided code. We've added a field
    # depth[], which is a stack, running in parallel, to opened[]. Depth[] 
    # tracks the depth of the node in the adjacent index.
    def depth_first(self, printStack = False):
        # Initializing opened[] and depth[] stacks
        # Opened = _init_state, depth = [0] (depth of init state is 0)
        self.opened.append(self.state_lst[0])
        self.depth.append(0)
        self.closed = []
        # Counter variable, for number of children checked thus far
        i = 0
        while(self.opened):
            # Incriment number of nodes checked thus far
            i+=1
            CS = self.opened.pop()
            # If we have found our desired goal state
            if(CS == _goal_state):
                # Show the user, and return to halt iteration
                # self.display()
                print("FOUND IT!");
                # If user runs with parameter True, print the stack of states.
                if(printStack):
                    self.display()
                    print('\n ---SOLUTION--- \n')
                for row in CS:
                    print(row)
                print("NUMBER OF CLOSED NODES: %d" %len(self.closed))
                print("NUMBER OF NODES CHECKED: %d" %i)
                return
            # If we haven't found our desired goal state
            else:
                # Add CS to closed, and gather the depth value of CS
                self.closed.append(CS)
                depth_value = self.depth.pop()
                # If CS is within our depth bound (depth < 5 in this case)
                if(depth_value < depth_limit):
                    # We generate our new states, stored in new_states
                    new_states = self.generate_states(self.state_lst.index(CS))
                    # Here, we remove all duplicate/previously checked states
                    # Duplicate states are in opened[] or closed[]
                    new_states_cleaned = [x for x in new_states if 
                        x not in self.opened and x not in self.closed]
                    # We push all of our new child states to self.opened[],
                    # And push all child depth values to self.depth[] (CS + 1)
                    for each in new_states_cleaned:
                        self.opened.append(each)
                        self.depth.append(depth_value + 1)
        

    #returns (row,col) of value in state indexed by state_idx  
    def find_coord(self, value, state_idx):
        for row in range(3):
            for col in range(3):
                if self.state_lst[state_idx][row][col] == value:
                    return (row,col)
                
    #returns list of (row, col) tuples which can be swapped for blank
    #these form the legal moves of state state_idx within the state list 
    def get_new_moves(self, state_idx):
        row, col = self.find_coord(0,state_idx) #get row, col of blank
        moves = []
        if row < 2:
            moves.append((row + 1, col)) # move from the bottom
        if col < 2:
            moves.append((row, col + 1)) # move from the right
        if row > 0:
            moves.append((row - 1, col))  #move from directly above
        if col > 0:
            moves.append((row, col - 1))  #move from the left
        return moves


    #Generates all child states for the state indexed by state_idx
    #in the state list.  Appends child states to the list
    #
    # NOTE: In addition to provided functionality, function now also returns
    # a list, containing all generated child states. This is done so that,
    # rather than track each individual child, we can append each item in our
    # returned list to self.opened[] upon returning.
    def generate_states(self,state_idx):
        #get legal moves
        move_lst = self.get_new_moves(state_idx)
        
        #find coordinates of the blank position
        blank = self.find_coord(0,state_idx)

        #shift the blank and tile to be moved for each move 
        #append resulting state to the state list
        copy_move_lst = []
        for tile in move_lst:
            #create a new state using deep copy 
            #ensures that matrices are completely independent
            clone = deepcopy(self.state_lst[state_idx])

            #move tile to position of the blank
            clone[blank[0]][blank[1]] = clone[tile[0]][tile[1]]

            #set tile position to 0                          
            clone[tile[0]][tile[1]] = 0
            
            #append child state to the list of states.
            self.state_lst.append(clone)
            copy_move_lst.append(clone)
        return copy_move_lst

def main():
    p = EightPuzzle()
    p.depth_first()


if __name__ == "__main__":
    main()
