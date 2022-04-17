import node 
import numpy as np
import csv
import pandas
from enum import IntEnum
import math


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values #returned as two-dimensional data structure with labeled axes.
        #print(self.raw_data)
        self.nd_dict = dict()
        self.num_rows = self.raw_data.shape[0]
        self.endNodes = []
        self.startPoint = 4
        for i in range (self.num_rows) :
            tmpNode = node.Node(self.raw_data , i+1)
            if tmpNode.checkIfEnd():
                self.endNodes.append(i+1)
            self.nd_dict[i+1] = tmpNode
            #print(self.nd_dict[i])
        #for i in range (self.num_rows) :
        #    print(self.nd_dict[i+1].getSuccessors())

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        if self.inEndNodes(self.startPoint):
            self.endNodes.remove(self.startPoint)
        return self.nd_dict[self.startPoint]

    def getNodeDict(self):
        return self.nd_dict

    def getEndNodes(self):
        return self.endNodes    

    def setStartPoint(self , index):
        self.startPoint = index
        return

    def BFS(self, nd):
        cnt=0
        queue = [[float(nd),0,0]]
        nodeList = []
        DirectionList = []
        parentList = []
        records = [float(nd)]

        while len(queue)!=0:
            tmplist = queue.pop(0)[:]
            tmpNode = self.nd_dict[tmplist[0]]
            if tmpNode.getSuccessorNumbers()==1 and tmplist[0]!=nd and self.inEndNodes(tmplist[0]):
                destination = tmplist[0]
                self.endNodes.remove(destination)
                #shortestPath = [float(tmplist[0])]
                Path = []
                while tmplist[0]!=nd:
                    for j in range(cnt):
                        if nodeList[j]==tmplist[0]:
                            tmplist[0] = parentList[j]
                            tmplist[1] = DirectionList[j]
                            #shortestPath.append(float(tmplist[0]))
                            #print(tmplist)
                            Path.append(tmplist[1])
                            #print(Path)
                            cnt = j
                            break
                #shortestPath.reverse()
                Path.reverse()
                return destination , Path
            else :
                for i in range (tmpNode.getSuccessorNumbers()):
                    inRecord=False
                    for record in records :
                        if record == tmpNode.getSuccessors()[i][0]:
                            inRecord=True
                            break
                    if not inRecord :
                        queue.append(tmpNode.getSuccessors()[i])
                        nodeList.append(tmpNode.getSuccessors()[i][0])
                        DirectionList.append(tmpNode.getSuccessors()[i][1])
                        parentList.append(tmplist[0])
                        records.append(tmpNode.getSuccessors()[i][0])
                        cnt+=1
                        
                        
        
    # #     # TODO : design your data structure here for your algorithm
    # #     # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
    #     return None

    def BFS_2(self, nd_from, nd_to):
        cnt=0
        queue = [[float(nd_from),0,0]]
        nodeList = []
        DirectionList = []
        parentList = []
        records = [float(nd_from)]

        
        while len(queue)!=0:
            print(records)
            tmplist = queue.pop(0)[:]
            tmpNode = self.nd_dict[tmplist[0]]
            for i in range (tmpNode.getSuccessorNumbers()):
                inRecord=False
                for record in records :
                    if record == tmpNode.getSuccessors()[i][0]:
                        inRecord=True
                        break
                if not inRecord :
                    queue.append(tmpNode.getSuccessors()[i])
                    nodeList.append(tmpNode.getSuccessors()[i][0])
                    DirectionList.append(tmpNode.getSuccessors()[i][1])
                    parentList.append(tmplist[0])
                    records.append(tmpNode.getSuccessors()[i][0])
                    cnt+=1
                    #print(tmpNode.getIndex())
                    if tmpNode.getSuccessors()[i][0] == nd_to:
                        tmplist = tmpNode.getSuccessors()[i][:]
                        shortestPath = [float(nd_to)]
                        Path = []
                        while tmplist[0]!=nd_from:
                            for j in range(cnt):
                                if nodeList[j]==tmplist[0]:
                                    tmplist[0] = parentList[j]
                                    tmplist[1] = DirectionList[j]
                                    shortestPath.append(float(tmplist[0]))
                                    #print(tmplist)
                                    Path.append(tmplist[1])
                                    #print(Path)
                                    cnt = j
                                    break
                        
                        shortestPath.reverse()
                        Path.reverse()
                        print(shortestPath , Path)
                        #print(records)
                        return (shortestPath , Path)
                        
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

    def get_Direction(self , directions) :
        lst = []
        for dir in directions :
            if dir == 0:
                lst.append('1')
            elif dir == 1:
                lst.append('3')
            elif dir == 2:
                lst.append('4')
            elif dir == 3:
                lst.append('2')
        return lst
            
    def inEndNodes(self , nodeIndex) :
        for endNode in self.endNodes :
            if endNode==nodeIndex :
                return True
        return False
