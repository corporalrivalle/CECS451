from board import Board
import time
import numpy as np

#Derek Zhang, 026225028

#general idea is as follows
#1. on each queen, find all possible moves
#2. for each move, find whether alpha (number of queens attacking) decreases
#   if decrease, make that move
#   if no decrease, move on to next move
#   if decreases for all moves, start from the first queen again to see if any better solution is available
#   if no decrease for all moves, move on to next queen
#3. if no decrease for all queens, re roll the board

def hill_climbing(board):
    current_board = board
    current_fitness = current_board.get_fitness()
    if current_fitness == 0:
        return current_board
    next_board = current_board
    while True:
        try:
            queens_list = find_queens(current_board)
            #iterate through every queen in the list
            for queen in queens_list:
                q_alpha = find_alpha(current_board, queen)
                #find all possible moves for specific queen
                legal_moves = possible_moves(current_board, queen)
                #iterate through all possible moves
                next_board.flip(queen[0], queen[1])
                for move in legal_moves:
                    #find the alpha of that move
                    alpha = find_alpha(next_board, move)
                    if alpha < q_alpha:
                        #if the alpha is lower than the current alpha, make the move
                        next_board.flip(move[0], move[1])
                        current_board = next_board
                        #if the fitness is 0, return the board
                        if current_board.get_fitness() == 0:
                            return current_board
                        # print("New Alpha: ", alpha)
                        # print("Previous Alpha: ", q_alpha)
                        raise NewSolutionException
                    else:
                        #if the alpha is higher than the current alpha, move on to the next move
                        pass
                #places queen back to original position if no better solution is found
                next_board.flip(queen[0], queen[1])
            #if no better solution is found, re roll the board
            if current_board.get_fitness() == 0:
                return current_board
            else:
                raise CatastrophicFailure
        except NewSolutionException: #flags if a new solution is found
            # print("New Solution found!")
            # current_board.show_map()
            # print("New fitness: ", current_board.get_fitness())
            pass
        except CatastrophicFailure: #flags if no better solution is found
            return current_board
        
class NewSolutionException(Exception):
    pass

class CatastrophicFailure(Exception):
    pass

#finds all queens on the board
def find_queens(board):
    queens = []
    for i in range(board.n_queen):
        for j in range(board.n_queen):
            if board.map[i][j] == 1:
                queens.append([i,j])
    return queens

#returns possible moves for a specific queen
def possible_moves(board, queen):
    movelist=[]
    queen_row = queen[0]
    # for i in range(-1,2):
    for k in range(-1,2):
        if k==0:
            #skip the queen itself
            pass
        else:
            if (k+queen[1]<0):
                #skip if out of bounds
                pass
            else:
                try:
                    if board.map[queen_row][k + queen[1]] == 0:
                        movelist.append([queen_row, k + queen[1]])
                except IndexError:
                    pass
            

    return movelist


#finds the alpha for a specific queen (number of queens attacking)
def find_alpha(board, queen):
    alpha = 0
    #check the entire board for queens
    for i in range(board.n_queen):
        for j in range(board.n_queen):
            if board.map[i][j] == 1:
                if i==queen[0] and j==queen[1]:
                    #skip the queen itself
                    pass
                else:
                    #check if queen is in the same row
                    if i == queen[0]:
                        alpha += 1
                    #check if queen is in the same column
                    elif j == queen[1]:
                        alpha += 1
                    #check if queen is in the same diagonal
                    elif abs(i-queen[0]) == abs(j-queen[1]):
                        alpha += 1
    return alpha
                

def test_function(board_size,stime):
    test = Board(board_size)
    original = np.copy(test.map)
    solution= hill_climbing(test)
    if solution.get_fitness() == 0:
        print("Time taken: ", time.time()-stime)
        print(original)
        solution.show_map()
        return False
    else:
        return True
    
def main(board_size):
    invalid_test = True
    restarts = 0
    stime = time.time()
    while invalid_test and restarts<1000:
        invalid_test=test_function(board_size, stime)
        restarts +=1
    if restarts == 1000:
        print("No solution found after 1000 restarts.")
    else:
        print("Solution found after {} restarts.".format(restarts))

if __name__ == "__main__":
    input_size = int(input("Enter board size: "))
    main(input_size)


