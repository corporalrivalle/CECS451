from board import Board

def hill_climbing(board, max_restarts):
    restarts = 0
    while restarts < max_restarts:
        
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
    for i in range(-1,2):
        for k in range(-1,2):
            if k==0 and i==0:
                #skip the queen itself
                pass
            else:
                if (k+queen[1]<0) or (i+queen_row<0):
                    #skip if out of bounds
                    pass
                else:
                    try:
                        if board.map[i + queen_row][k + queen[1]] == 0:
                            movelist.append([i + queen_row, k + queen[1]])
                    except IndexError:
                        pass





def test_function():
    test = Board(8)
    solution= hill_climbing(test)
    if solution == "failed":
        return True
    else:
        test.show_map()
        solution.show_map()
        return False