import random
import numpy as np
from board import Board

def hill_climbing(board, max_restarts):
    restarts = 0
    while restarts < max_restarts:
        current_board = board  # Start from a random initial state
        current_fitness = current_board.get_fitness()

        # Perform hill climbing until a local optimum is reached
        while True:
            neighbors = []  # Store neighboring boards
            for i in range(current_board.n_queen):
                for j in range(current_board.n_queen):
                    if current_board.get_map()[i][j] == 1:
                        continue  # Skip current queen

                    # Create a neighbor by flipping a queen at (i, j)
                    neighbor_board = current_board.copy()  # Implement a copy method in your Board class
                    neighbor_board.flip(i, j)
                    neighbor_fitness = neighbor_board.get_fitness()
                    neighbors.append((neighbor_board, neighbor_fitness))

            if not neighbors:
                break  # No better neighbors, local optimum reached

            # Select the best neighbor
            best_neighbor, best_neighbor_fitness = max(neighbors, key=lambda x: x[1])

            if best_neighbor_fitness <= current_fitness:
                break  # Local optimum reached

            current_board = best_neighbor
            current_fitness = best_neighbor_fitness

        if current_fitness == 0:
            return current_board  # Solution found

        # Randomly restart if no solution found
        restarts += 1
        board = Board(board.n_queen)  # Generate a new random initial state

    return None  # No solution found within max_restarts

if __name__ == '__main__':
    max_restarts = 100  # Adjust this as needed
    test = Board(8)  # Set the size of the board (e.g., 8-Queens)
    solution = hill_climbing(test, max_restarts)

    if solution:
        print("Solution found:")
        solution.show_map()
    else:
        print("No solution found after {} restarts.".format(max_restarts))