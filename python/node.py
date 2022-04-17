import math
from cmath import nan
from enum import IntEnum

# You can get the enumeration based on integer value, or make comparison
# ex: d = Direction(0), then d would be Direction.NORTH
# ex: print(Direction.SOUTH == 0) should return False
class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    WEST  = 2
    EAST  = 3

# Construct class Node and its member functions
# You may add more member functions to meet your needs
class Node:
    def __init__(self, map , index=0):
        self.index = index
        self.map = map
        self.Successors = []
        # store successor as (Node, direction to node, distance)
        for i in range (4) :
            if not ( math.isnan(map[index-1][i+1]) ):
                self.Successors.append([map[index-1][i+1],Direction(i),map[index-1][i+5]])
            #print (self.Successors[i])
        self.isEnd = self.checkIfEnd()       

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


    def getDirection(self, nd):
        # TODO : if nd is adjacent to the present node, return the direction of nd from the present node
		# For example, if the direction of nd from the present node is EAST, then return Direction.EAST = 4
		# However, if nd is not adjacent to the present node, print error message and return 0 
        return

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd: 
                return True
        return False

