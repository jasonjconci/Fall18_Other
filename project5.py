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
def print_matrix(matrix, source_string, target_string):
    target_string = " " + target_string
    for i,row in enumerate(matrix[::-1]):
        if i != len(target_string):
            print(target_string[len(target_string)-1-i]),
        for each in row:
            each.print_cell(),
        print
    print "     ",
    #source_string = "  "  + source_string
    for i in source_string:
        print "   " + i,
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
        matrix[0][i].directions = ["DEL"]
    for j in range(m+1):
        matrix[j][0].score = j
        matrix[j][0].directions = ["INS"]
    print "EMPTY MATRIX"
    print_matrix(matrix, str_one, str_two)

    for i in range(1, m+1):
        for j in range(1, n+1):
            matrix = input_score_and_pointers(matrix, i, j, str_one, str_two)
    print "COMPLETED MATRIX"
    print_matrix(matrix, str_one, str_two)
    get_alignment_backtrace(matrix, str_one, str_two)


def get_alignment_backtrace(matrix, source_string, target_string):
    n = len(source_string)
    m = len(target_string)
    node = matrix[m][n]  
    source_string_ls = []
    target_string_ls = []
    op_ls = []

    print "Minimum edit distance score:", node.score
    
    while n > 0 or m > 0:
        children = matrix[m][n].directions
        if SUB in children and m > 0 and n > 0:
            if source_string[n-1] != target_string[m-1]:
                op_ls.insert(0, SUB)
            else:
                op_ls.insert(0, ' ')
            source_string_ls.insert(0, source_string[n-1])
            target_string_ls.insert(0, target_string[m-1])
            n -=1
            m -= 1
        elif DEL in children and n > 0:
            op_ls.insert(0,DEL)
            source_string_ls.insert(0, source_string[n-1])
            target_string_ls.insert(0, "#")
            n -= 1
        elif INS in children and m > 0:
            op_ls.insert(0, INS)
            source_string_ls.insert(0, "#")
            target_string_ls.insert(0, target_string[m-1])
            m -= 1
    
    for i in range(len(target_string_ls)):
        print source_string_ls[i],
        print " - ",
        print target_string_ls[i],
        print op_ls[i]

def main(strargs):
    print("Hello world!")
    str_one = strargs[0]
    str_two = strargs[1]
    create_matrix(str_one, str_two)


# allows us to easily run at command line, "python project5.py arg1 arg2 ..."
if __name__ == "__main__":
    #print sys.argv[1:]
    main(["intention", "execution"])
