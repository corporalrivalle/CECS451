import random
from board import Board
import time
class gBoard: #A board's genetic representation
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.DNA = self.generate_DNA()
        self.fitness = self.board.get_fitness()
        self.probability = 0
        self.truncprob = 0

    def generate_DNA(self):
        DNA=[]
        for list in self.board.map:
            for j in range(len(list)):
                if list[j] == 1:
                    DNA.append(j)
        return DNA

    def get_fitness(self):
        return self.board.get_fitness()
    
    def selectability(self):
        return 1.4**(28-self.get_fitness())
            


def genetic(max_generations):
    # Initialize the population randomly
    population = []
    pop_count = 10
    for _ in range(pop_count):
        population.append(gBoard(8))

    
    # Evolve the population
    for generation in range(max_generations):
        # print("Generation", i)
        # Check if a solution is found
        for individual in population:
            # print(individual.DNA, individual.get_fitness())
            if individual.get_fitness() == 0:
                print("Solution found on generation", generation)
                return individual


        #sort population to try and breed best individuals
        population.sort(key=lambda x: x.get_fitness())
        totals = 0
        #finds total selectability of population
        for individual in population:
            totals += individual.selectability()
        #finds probability of each individual being selected
        for individual in population:
            individual.probability = individual.selectability()/totals
            individual.truncprob = int(individual.probability*100)
            # print(individual.DNA, individual.probability, individual.get_fitness(), individual.selectability(), individual.truncprob)
        #selects 4 pairs of parents based on probability
        parents = []
        for _ in range(pop_count):
            parents.append(parent_pairing(population))
        next_generation = []
        for parent_pair in parents:
            # print("Parents:",parent_pair[0].DNA, parent_pair[1].DNA)
            child = crossover(parent_pair[0], parent_pair[1])
            # print("Child:", child.DNA, child.get_fitness())
            next_generation.append(child)
        
        population = next_generation
        
        #mutation chance here

        mutation_chance = random.randint(0,4)
        for individual in population:
            mutation = random.randint(0,4)
            if mutation == mutation_chance:
                # print("Mutation!")
                individual=mutate(individual)
        
        # print("New Generation")
        for individual in population:
            if individual.get_fitness() == 0:
                print("Solution found on generation", generation)
                return individual
            # print(individual.DNA, individual.get_fitness())
        
    print("Failed to find a successful solution within 1000 generations.")
    print("Best solution found:")
    population.sort(key=lambda x: x.get_fitness())
    population[0].board.show_map()
    print("Fitness:", population[0].get_fitness())
    return None  # No solution found within max_generations

def mutate(individual):
    random_row = random.randint(0,7)
    random_column = random.randint(0,7)
    while random_column == individual.DNA[random_row]:
        random_column = random.randint(0,7)
    individual.board.flip(random_row, random_column)
    # print("Mutated row", random_row, random_column,"to 1")
    individual.board.flip(random_row, individual.DNA[random_row])
    # print("Flipped", random_row,individual.DNA[random_row], "back to", 0)
    individual.DNA[random_row] = random_column
    individual.fitness = individual.board.get_fitness()
    individual.probability = 0
    individual.truncprob = 0
    return individual


def parent_pairing(population):
    pair=[]
    pairing=True
    while pairing:
        random_number = random.randint(0,100)

        #need to make a way to select parents based on probability
        prob_list = []
        for individual in population:
            prob_list.append(individual.truncprob)
        
        if len(set(prob_list)) == 1:
            pair.append(population[0])
            pair.append(population[1])
            break

        while random_number > 0:
            for number in prob_list:
                random_number -= number
                if random_number <= 0:
                    pair.append(population[prob_list.index(number)])
        if len(pair) >=2:
            pairing=False
    return pair



def crossover(self, other):
    crossover_point = random.randint(2,5)
    child = gBoard(8)
    new_map = []
    new_dna = self.DNA[0:crossover_point] + other.DNA[crossover_point:]
    # print("New DNA:", new_dna)
    for i in range(8):
        new_map.append([0,0,0,0,0,0,0,0])
    for i in range(8):
        new_map[i][new_dna[i]] = 1
    child.board.map = new_map
    # print("New Child Map")
    # child.board.show_map()
    # print("Reference Map")
    # print(new_map)
    child.fitness = child.board.get_fitness()
    child.DNA = new_dna
    return child
    # Swap DNA sequences beyond the crossover point
    


def test_function():
    print("Starting algorithm...")
    print("Parameters: \n Max Generations: 1000 \n Population Size: 10 \n Mutation Chance: 25% \n Crossover Point: Random between 2-5")
    stime = time.time()
    result = genetic(1000)
    print("Time taken: ", time.time()-stime)
    if result != None:
        print("Solution found:")
        result.board.show_map()
    else:
        print("No solution found after 1000 generations.")
    

test_function()
