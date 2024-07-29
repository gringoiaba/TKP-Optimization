import numpy as np
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
        bids with the highest price are added to the solution until it's unfeasible """
    def init(self):

        time_demand = [0]*self.max_time
        solution = [0]*self.n 

        for _ in range(self.n):
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
    
    def lahc(self, t, iterations):
        s = self.solution
        cost = self.cost
        l = [cost]*t
        best_solution = s
        best_value = cost

        i = 0
        k = 0

        while k < iterations:
            for solution in self.one_flip(s):
                cost = self.evaluate(solution)
                prev_cost = self.evaluate(s)
                v = i%t
                
                if cost > 0:
                    i += 1
                    if (cost >= prev_cost) or (cost >= l[v]):
                        s = solution
                        l[v] = cost
                        if cost > best_value:
                            best_solution = solution
                            best_value = cost   
                
            k += 1
        
        self.solution = best_solution
        self.cost = best_value


    def __str__(self) -> str:
        pass
    
def main(file, iterations):
    start = timer()
    solver = Solver(file)
    initial = solver.cost
    solver.lahc(10, iterations)
    end = timer()
    print(f"{file}, {iterations}, {initial}, {solver.cost}, {end-start}")

if __name__ == "__main__":
    files = ["U2", "U100", "I5", "I25", "I72", "I90", "I100", "HB"]
    seed = seed(0)
    n = 10
    print(f"instance, iterations, initialSolution, bestSolution, time")
    iterations = [i*50 for i in range(1,n+1)]
    """for i in iterations:
        for file in files:
            main(file, i)
        """
    main("U2", 5)
        
    