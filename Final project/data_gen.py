from numpy import random
from random import randint
if __name__ == "__main__" :

    for n in range(10,110, 10) :
        path = "./Data/test" + str(n) + ".txt"
        file = open(path, "w")
        file.write(str(n) + "\n")
        end = 0
        for i in range(n) :
            desk = random.poisson(2)+1
            start = randint(1,n)
            end = start + random.poisson(2)
            file.write(str(desk) + " " + str(start) + " "  + str(end) + "\n")
        file.close()