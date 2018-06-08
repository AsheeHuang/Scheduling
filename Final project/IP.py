from gurobipy import *

M = 1000
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
def interval(flight, flight2) :
    return [max(flight.start, flight2.start)-1, min(flight.end, flight2.end)-1]

if __name__ == "__main__" :
    flights = read_data("./Data/test2.txt")
    for f in flights :
        print(f.overlap)

    m = Model()

    T = max(flights, key = lambda x : x.end).end #find max time index
    n = len(flights)
    R = sum(f.desk for f in flights)

    #set variable
    D = m.addVar(lb = 0 , ub = R ,vtype = GRB.INTEGER, name = 'D')
    y = m.addVars(n,T,R, vtype = GRB.BINARY, name = 'y')
    z = m.addVars(n,n,vtype = GRB.BINARY, name = 'z')

    #set objective
    m.setObjective(D, GRB.MINIMIZE)

    #set constraints
    for j in range(n) :
        for t in range(flights[j].start-1, flights[j].end) :
            cons1 = LinExpr()
            for r in range(flights[j].desk-1,R) :
                cons1.add(y[j,t,r],r)
            m.addConstr(cons1 <= D, name = 'cons1')

    for j in range(n) :
        for t in range(flights[j].start-1, flights[j].end) :
            cons2 = LinExpr()
            for r in range(flights[j].desk-1,R) :
                # print(j,t,r)
                cons2.add(y[j,t,r])
            m.addConstr(cons2 == 1, name = 'cons2')

    for j in range(n) :
        for t in range(flights[j].start-1, flights[j].end-1) :
            for r in range(flights[j].desk-1,R) :
                m.addConstr(y[j,t,r] == y[j,t+1,r])


    for i in range(n) :
        for j in flights[i].overlap :
            m.addConstr(z[i,j] + z[j,i] == 1)

    for i in range(n) :
        for j in flights[i].overlap :
            time_interval = interval(flights[i],flights[j])
            for t in range(time_interval[0],time_interval[0]+1) :  # maybe we don't consider the whole time interval
                expr = LinExpr()
                expr2 = LinExpr()
                for r in range(flights[j].desk-1, R) :
                    expr.add(y[j,t,r],r)
                for r in range(flights[i].desk-1, R) :
                    expr2.add(y[i,t,r],r)
                m.addConstr(expr + flights[i].desk <= expr2 + M * (z[i,j]))
                m.addConstr(expr2 + flights[j].desk <= expr + M * (1-z[i, j]))

    # for j in range(n) :
    #     for i in flights[j].overlap :
    #         time_interval = interval(flights[i],flights[j])
    #         for t in range(time_interval[0],time_interval[1]) :  # maybe we don't consider the whole time interval
    #             expr = LinExpr()
    #             expr2 = LinExpr()
    #             for r in range(flights[j].desk-1, R) :
    #                 expr.add(y[j,t,r],r)
    #             expr.add(flights[i].desk)
    #             for r in range(flights[i].desk-1, R) :
    #                 expr2.add(y[i,t,r],r)
    #             expr2 += (M*(1-z[i,j]))
    #             m.addConstr(expr <= expr2)


    m.optimize()    #
    obj = int(m.objVal)
    flight_table = [[0 for _ in range(T)] for _ in range(obj + 1)]

    for j in range(n):
        for t in range(T):
            for r in range(obj + 1):
                if y[j, t, r].getAttr('X') == 1:
                    for r_ in range(r, r - flights[j].desk, -1):
                        flight_table[r_][t] = j + 1

    for line in flight_table:
        print(line)

