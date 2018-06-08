from random import sample
from copy import copy
from time import time
class Flight:
    def __init__(self,index, desk, start, end):
        self.index = index
        self.desk = desk
        self.start = start
        self.end = end
        #self.interval = end - start
        self.interval = [start,end]
        self.overlap = []
    def interval_overlap(self,flight2):
        if(self.end < flight2.start or self.start > flight2.end):
            return False
        return True

def read_data(path) :
    data = open(path, "r")
    n = int(data.readline())
    lines = data.read().splitlines()
    flights = []
    for i in range(len(lines)) :
        line = lines[i].split(" ")
        flight = Flight(i+1, int(line[0]), int(line[1]), int(line[2]))
        flights.append(flight)
    for i in range(len(flights)) :
        for j in range(i+1,len(flights)) :
            if flights[i].interval_overlap(flights[j])  :
                flights[i].overlap.append(j)
                flights[j].overlap.append(i)

    return flights
def create_table(flights,sol) :
    T = max(flights, key = lambda x : x.end).end #find max time index
    R = sum(f.desk for f in flights)

    flights_table = [[0 for _ in range(T)] for _ in range(R)]

    for i in range(len(sol)) :
        start = flights[sol[i]].start
        end = flights[sol[i]].end
        desk = flights[sol[i]].desk

        r = R -desk
        # print(start, end)
        repeat = True
        while r != 0 and repeat:

            for t in range(start-1,end) :
                if flights_table[r-1][t] != 0 :
                    r += 1
                    repeat = False
                    break
            r -= 1

        for d in range(r,r+desk) :
            for t in range(start-1 , end) :
                flights_table[d][t] = sol[i]+1
        # print()
    for i in range(len(flights_table)):
        if all(j == 0 for j in flights_table[i]) :
            flights_table = flights_table[0:i]
            break

    return flights_table

def print_table(flights_table):
    for i in flights_table :
        print(i)

def swap(sol, A, B) :
    temp = sol[A]
    sol[A] = sol[B]
    sol[B] = temp

if __name__ == "__main__" :

    for n in range(10,110,10) :
        flights = read_data('./Data/test'+str(n)+'.txt')
        start_time = time()
        n = len(flights)
        sol = dict((i,i) for i in range(n))


        flights_table = create_table(flights,sol)
        best_sol = (list(sol), len(flights_table))
        curr_sol = (sol, len(flights_table))

        tabu_len = 5
        tabu_list = []
        count = 0

        while count < 1000 :
            swap_pair = sample([i for i in range(n)], 2)
            swap_pair = (min(swap_pair), max(swap_pair)) #randomly choose 2 flight swap

            if swap_pair not in tabu_list :
                swap(sol, swap_pair[0], swap_pair[1])
                flights_table = create_table(flights, sol)
                curr_sol = (sol, len(flights_table))

                if curr_sol[1] < best_sol[1] :
                    best_sol = (copy(curr_sol[0]), curr_sol[1])

                tabu_list.append(swap_pair)
                if len(tabu_list) > tabu_len :
                    tabu_list.pop(0)
            count += 1
        print('------Flight num = %d--------' %n)
        print("Time : %.2f sec." % (time() - start_time))
        # flights_table = create_table(flights,best_sol[0])
        # print_table(flights_table)
        print("Minimum desk num :" , best_sol[1])







