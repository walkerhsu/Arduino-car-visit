import node 
import numpy as np
import csv
import pandas
import math

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
        self.startPoint = 1
        self.visited = []
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
            self.visited.append(self.startPoint)
        return self.nd_dict[self.startPoint]

    def getNodeDict(self):
        return self.nd_dict

    def getEndNodes(self):
        return self.endNodes    

    def setStartPoint(self , index):
        self.startPoint = index
        return

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

    def strategy_3(self , start):
        return self.Dijkstra(start)

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

    def getHowToGo(self , nd_start , nd_end , lst) :
        #lst : index , distance , parent , father
        currentStep = nd_end
        direction_path = []
        while nd_start != currentStep:
            for ls in lst :
                if ls[0]==currentStep:
                    if currentStep == nd_end : 
                        total_distance = ls[1]
                    currentStep = ls[2]
                    direction_path.append(ls[3])
                    break
        direction_path.reverse()
        movement = self.get_Direction(direction_path)
        return total_distance , movement

    def TurnOrNot(self , dir1 , dir2):
        if (dir1==dir2):
            return 0
        elif (dir1!=dir2) :
            return 1

    def Dijkstra(self , start) :
        queue = []
        records = []
        for i in range(self.num_rows):
            if (i+1) == start:
                queue.append([i+1 , 0 , -1 , -1 , -1][:]) #index , shortestDistance , parent , direction , turns
            else:
                already_visited = False
                for visited in self.visited:
                    if (i+1) == visited :  
                        already_visited = True
                        break
                if not already_visited :
                    queue.append([i+1 , 10E6 , -1 , -1 , 10E6][:])
        #print(queue)
        while len(queue)!=0 :
            # print("---------------------------------------------")
            # for q in queue:
            #     print(q)
            distance , turns = 10E6 , 10E6
            shortest = []
            for list in queue :
                if list[1]<distance:
                    shortest = list
                    distance = list[1]
                    turns = list[4]
                elif list[1]==distance:
                    if list[4]<turns:
                        shortest = list
                        turns = list[4]
            # print(shortest)

            queue.remove(shortest)
            tmpNode = self.nd_dict[shortest[0]]
            sucessors = tmpNode.getSuccessors()
            
            for suc in sucessors:
                pos=-1
                for i in range(len(queue)):
                    if queue[i][0]==int(suc[0]) :
                        pos = i
                if pos!=-1 and (suc[2] + shortest[1] < queue[ pos ][1]):
                    queue[ pos ][1] = suc[2] + shortest[1]
                    queue[ pos ][2] = shortest[0]
                    queue[ pos ][3] = suc[1]
                    queue[ pos ][4] = shortest[4] + self.TurnOrNot(shortest[3] , suc[1])
                elif pos!=-1 and (suc[2] + shortest[1] == queue[ pos ][1]):
                    if shortest[4] + self.TurnOrNot(shortest[3] , suc[1]) < queue[ pos ][4] : 
                        queue[ pos ][4] = shortest[4] + self.TurnOrNot(shortest[3] , suc[1])
                        queue[ pos ][1] = suc[2] + shortest[1]
                        queue[ pos ][2] = shortest[0]
                        queue[ pos ][3] = suc[1]
            records.append(shortest[:])
            if self.inEndNodes(shortest[0]): 
                self.endNodes.remove(shortest[0])
                self.visited.append(shortest[0])
                return shortest[0] , records

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