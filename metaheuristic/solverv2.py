import numpy as np
import copy
from timeit import default_timer as timer

class Solution():

    def __init__(self, solution, time_demand, cost) -> None:
        self.solution = solution
        self.time_demand = time_demand
        self.cost = cost

    def flip_bid(self, index, data):
        if self.solution[index]:
            self.solution[index] = 0
            for t in range(data.start[index]-1, data.finish[index]):
                self.time_demand[t] -= data.demand[index]
            self.cost -= data.price[index]
        
        else:
            self.solution[index] = 1
            for t in range(data.start[index]-1, data.finish[index]):
                self.time_demand[t] += data.demand[index]
                if self.time_demand[t] > data.capacity:
                    self.cost = -1
                    return
            self.cost += data.price[index]

    def __str__(self) -> str:
        return str(self.solution)

class Data():
    def __init__(self, file) -> None:
        n, capacity, price, demand, start, finish = self.read_file(file) 
        self.n = n
        self.capacity = capacity
        self.price = price
        self.demand = demand
        self.start = start
        self.finish = finish
        self.max_time = max(finish)

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
                bid = line.split(' ')
                bid.pop()
                bid = [int(i) for i in bid]

                price.append(bid[0])
                demand.append(bid[1])
                start.append(bid[2])
                finish.append(bid[3])

        return n, capacity, price, demand, start, finish


class Solver():

    def __init__(self, data: Data):
        self.data = data
        self.solution = self.init()
    
    """ Creates an initial solution to the TKP 
        bids with the highest price are added to the solution until it's unfeasible """
    def init(self):

        n = self.data.n
        price = self.data.price
        demand = self.data.demand
        start = self.data.start
        finish = self.data.finish
        capacity = self.data.capacity

        time_demand = [0]*self.data.max_time
        solution = [0]*n
        # List of indexes ordered from descending price 
        top_prices = np.argsort(price)[::-1]
        cost = 0

        for i in top_prices:
            # Jump bids with a demand higher than the max capacity
            if demand[i] > capacity:
                continue
            # Builds the time_demand array for each bid
            for t in range(start[i]-1, finish[i]):
                time_demand[t] += demand[i]
                if time_demand[t] > capacity:
                    for j in reversed(range(start[i]-1, t+1)):
                        time_demand[j] -= demand[i]
                    return Solution(solution, time_demand, cost)
                    
            # If the contraints are met, adds the bid to the solution
            solution[i] = 1
            cost += price[i]
        
        return Solution(solution, time_demand, cost)
                

    """ The Neighborhood is defined by a flip of a bid in a solution 
        for every bid, remove the bid if its already in the current solution, add it otherwise"""
    def one_flip(self):
        neighborhood = []

        for i in range(self.data.n):
            s = copy.deepcopy(self.solution)
            s.flip_bid(i, self.data)
            if s.cost > 0:
                neighborhood.append(s)

        return np.array(neighborhood)
    
    def lahc(self, t, iterations):
        s = self.solution
        cost = self.solution.cost
        l = [cost]*t
        best_solution = s

        i = 0
        k = 0

        while k < iterations:
            for solution in self.one_flip():
                prev_cost = self.solution.cost
                cost = solution.cost
                v = i%t

                if (cost >= prev_cost) or (cost >= l[v]):
                    self.solution = solution
                    l[v] = cost
                    if cost > best_solution.cost:
                        best_solution = solution
                i += 1
            k += 1
        
        self.solution = best_solution


    def __str__(self) -> str:
        pass

def main(file, iterations):
    start = timer()
    data = Data(file)
    solver = Solver(data)
    solver.lahc(10, iterations)
    end = timer()
    return solver.solution.cost, (end-start)

if __name__ == "__main__":
    n = 3
    print(f"file, size, cost, time")
    iterations = [i*5 for i in range(1,n+1)]
    for i in iterations:
        cost, time = main("U100", i)
        print(f"U100, {i}, {cost}, {time}")
        
        
    