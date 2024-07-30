import numpy as np
import sys
from timeit import default_timer as timer
from random import randint, seed

class Solver():

    def __init__(self, file:str):
        n, capacity, price, demand, start, finish = self.read_file(file) 
        self.n = n
        self.capacity = capacity
        self.price = price
        self.demand = demand
        self.start = start
        self.finish = finish
        self.max_time = max(finish)
        self.solution = self.init()
        self.cost = self.evaluate(self.solution)

    """ Reads the instance file and return its content """
    def read_file(self, file:str):
        price = []
        demand = []
        start = []
        finish = []

        with open(file, encoding="utf-8") as f:
            n = int(f.readline())
            capacity = int(f.readline())

            for _ in range(n):
                line = f.readline()
                bid = line.strip().split(' ')
                bid = [int(i) for i in bid]

                price.append(bid[0])
                demand.append(bid[1])
                start.append(bid[2])
                finish.append(bid[3])

        return n, capacity, price, demand, start, finish
    
    """ Calculates the cost function of a solution 
         if solution is not feasible returns a negative number """
    def evaluate(self, solution):
        total_price = np.dot(np.array(solution), self.price)

        # Array that stores the demand of bids from solution
        # time_demand[t] represents the total demand in time t
        time_demand = [0]*self.max_time

        for i in range(self.n):
            if solution[i]:
                for t in range(self.start[i]-1, self.finish[i]):
                    time_demand[t] += self.demand[i]
                    # Checks if the constraints are met
                    if time_demand[t] > self.capacity:
                        return -1
        
        return total_price
    
    """ Creates an initial solution to the TKP 
        adds random bids to the solution until it's unfeasible """
    def init(self):

        time_demand = [0]*self.max_time
        solution = [0]*self.n 

        for j in range(self.n):
            i = randint(0, self.n-1)
            if not solution[i]:
                for t in range(self.start[i]-1, self.finish[i]):
                    time_demand[t] += self.demand[i]
                    if time_demand[t] > self.capacity:
                        return solution
                solution[i] = 1
        
        return solution

    """ The Neighborhood is defined by a flip of a bid in a solution 
        for every bid, remove the bid if its already in the current solution, add it otherwise"""
    def one_flip(self, solution):
        neighborhood = []

        for i in range(self.n):
            neighborhood.append(np.copy(solution))
            neighborhood[i][i] = 0 if neighborhood[i][i] else 1

        return np.array(neighborhood)
    
    """ LAHC meta-heuristic implementation """
    def lahc(self, t, iterations, start):
        s = self.solution
        cost = self.cost
        l = [cost]*t
        best_solution = s
        best_value = cost

        i = 0
        k = 0

        while k < iterations:
            # Searches in the neighborhood
            for solution in self.one_flip(s):
                cost = self.evaluate(solution)
                prev_cost = self.evaluate(s)
                v = i%t
                
                # If the solution is feasible
                if cost > 0:
                    i += 1
                    if (cost >= prev_cost) or (cost >= l[v]):
                        s = solution
                        l[v] = cost
                        if cost > best_value:
                            time = timer()
                            time = time - start
                            print(f"time: {time:.2f},  cost: {cost},  solution: \n{solution}")
                            best_solution = solution
                            best_value = cost   
                
            k += 1
        
        self.solution = best_solution
        self.cost = best_value

    
def solve(file, iterations):
    start = timer()
    solver = Solver(file)
    initial = solver.cost
    solver.lahc(100, iterations, start)
    end = timer()
    print(f"Instance {file}\n Number of iterations: {iterations}\n Cost of initial solution: {initial}\n Cost of best solution {solver.cost}\n Elapsed time: {end-start}")
    print(solver.solution)

if __name__ == "__main__":
    n = len(sys.argv)
    print(n)
    if n != 4:
        print("ERROR: Invalid parameters.\nUsage: python solver.py file_name seed num_of_iterations\n")
        exit(1)
    file = sys.argv[1]
    rng = int(sys.argv[2])
    iterations = int(sys.argv[3])
    seed(rng)
    solve(file, iterations)