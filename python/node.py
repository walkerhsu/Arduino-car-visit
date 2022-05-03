import math
from cmath import nan
from enum import IntEnum

# You can get the enumeration based on integer value, or make comparison
# ex: d = Direction(0), then d would be Direction.NORTH
# ex: print(Direction.SOUTH == 0) should return False
class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH  = 2
    WEST  = 3

# Construct class Node and its member functions
# You may add more member functions to meet your needs
class Node:
    def __init__(self, map , number , index=0):
        self.index = index
        self.map = map
        self.Successors = []
        # store successor as (Node, direction to node, distance)
        for i in range (4) :
            if not ( math.isnan(map[index-1-number][i+1]) ):
                dir = self.setDirection(i)
                self.Successors.append([map[index-1-number][i+1],Direction(dir),map[index-1-number][i+5]])
            #print (self.Successors[i])
        self.isEnd = self.checkIfEnd()       

    def setDirection(self , i):
        if i==0:
            return 0
        if i==1:
            return 2
        if i==2:
            return 3
        if i==3:
            return 1


    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return self.Successors

    def getSuccessorNumbers(self):
        return len(self.Successors)

    def checkIfEnd(self):
        return (self.getSuccessorNumbers() == 1)

    def setSuccessor(self, successor, direction, length=1):
        self.Successors.append((successor, Direction(direction), int(length)))
        print("For Node {}, a successor {} is set.".format(self.index, self.Successors[-1]))
        return

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd: 
                return True
        return False

