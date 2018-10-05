'''

INSERT HEADER HERE

'''

import sys


SUB = "SUB"
DEL = "DEL"
INS = "INS"

'''
Defining a cell class so we can store the backpointers
'''
class Cell:
    def __init__(self,  score=0, xcoord = 0, ycoord = 0):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.score = score
        self.directions = []

    # function to print the value of a cell
    def print_cell(self):
        print " %2d " % self.score,

    def print_cell_all(self):
        print " %2d " % self.score, self.xcoord, self.ycoord, self.directions

    def __eq__(self, other):
        return self.score == other.score and self.xcoord == other.xcoord and self.ycoord == other.ycoord

'''
Function fo printing out the matrix in the format specified in the book,
because the data structure I use is [0][0] is top left, not bottom left
'''
def print_matrix(matrix):
    for row in matrix[::-1]:
        for each in row:
            each.print_cell(),
        print


'''
Returns the cost of substitution, given two characters
'''
def calc_sub_cost(char_one, char_two):
    return 0 if char_one == char_two else 2


def input_score_and_pointers(matrix, i, j, str_one, str_two):
    ins_cost = matrix[i-1][j].score + 1
    del_cost = matrix[i][j-1].score + 1
    sub_cost = matrix[i-1][j-1].score + calc_sub_cost(str_one[j-1], str_two[i-1])

    matrix[i][j].score = min(ins_cost, del_cost, sub_cost)

    ''' I know there's gotta be a better way, but I don't want to find it right now '''

    # if they're all the same:
    if ins_cost == del_cost == sub_cost:
        matrix[i][j].directions = [INS, DEL, SUB]

    # if two are the same, other greater:
    elif ins_cost == del_cost < sub_cost:
        matrix[i][j].directions = [INS, DEL]
    elif ins_cost == sub_cost < del_cost:
        matrix[i][j].directions = [INS, SUB]
    elif del_cost == sub_cost < ins_cost:
        matrix[i][j].directions = [DEL, INS]

    # if one is lower than all others:
    elif ins_cost < del_cost and ins_cost < sub_cost:
        matrix[i][j].directions = [INS]
    elif del_cost < ins_cost and del_cost < sub_cost:
        matrix[i][j].directions = [DEL]
    elif sub_cost < ins_cost and sub_cost < del_cost:
        matrix[i][j].directions = [SUB]

    return matrix

def create_matrix(str_one, str_two):
    n = len(str_one)
    m = len(str_two)

    matrix = [[Cell(0, i, j) for i in range(n+1)] for j in range(m+1)]
    for i in range(n+1):
        matrix[0][i].score = i
    for j in range(m+1):
        matrix[j][0].score = j
    print_matrix(matrix)

    for i in range(1, m+1):
        for j in range(1, n+1):
            matrix = input_score_and_pointers(matrix, i, j, str_one, str_two)
    print
    print_matrix(matrix)
    depth_first_search(matrix)


def get_children(node):
    children = []
    directions = node.directions
    for each in directions:
        if each == SUB:
            children.append((node.xcoord - 1, node.ycoord - 1))
        if each == INS:
            children.append((node.xcoord - 1, node.ycoord))
        if each == DEL:
            children.append((node.xcoord, node.ycoord - 1))
    return children


'''
It seems, to me, computing the minimum alignment involves computing the shortest
path from M(n,m) to M(0,0). At any given point, as in the book, we can move down,
left, or diagonal. This algorithm is meant to emulate a breadth first search, as
a means of computing the backtrace.
'''
def depth_first_search(matrix):
    print "NODE EQUALS NODE",
    print matrix[0][0] == Cell(0,0,0), matrix[0][0].print_cell_all()
    n = len(matrix[0])
    m = len(matrix)
    print(n, m)
    node_init = matrix[n-1][m-1]
    state_list = []

    all_paths_list = dfs_recursive(matrix, node_init, state_list)

    all_paths_list = [i for i in all_paths_list if i!= []]
    for path in all_paths_list[0]:
        print "NEW PATH"
        for state in path:
            for step in state:
                print(step)
        print '\n\n'
    print(len(all_paths_list[0]))



def get_alignment_backtrace(matrix):
    print "NODE EQUALS NODE",
    print matrix[0][0] == Cell(0,0,0), matrix[0][0].print_cell_all()
    n = len(matrix[0])
    m = len(matrix)
    node = matrix[n-1][m-1]
    backtrace = []
    while node != Cell(0,0,0):
        children = get_children(node)
        backtrace.append(node.directions[0])
        node = matrix[children[0][0]][children[0][1]]


'''
def dfs_recursive(matrix, node, state_list):
    state_list.append(node)
    # If we're at the end, just return the state list
    if node == Cell(0,0,0):
        return state_list
    else:
        children = get_children(node)
        if children == []:
            return
        child_nodes = [matrix[child[0]][child[1]] for child in children]
        return [dfs_recursive(matrix, child, state_list) for child in child_nodes]
'''

def main(strargs):
    print("Hello world!")
    str_one = strargs[0]
    str_two = strargs[1]
    create_matrix(str_one, str_two)


# allows us to easily run at command line, "python project5.py arg1 arg2 ..."
if __name__ == "__main__":
    print sys.argv[1:]
    main(sys.argv[1:])