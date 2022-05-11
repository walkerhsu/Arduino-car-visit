from pickle import TRUE
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
        self.rows = 3
        self.columns = 3
        self.cntPassNode = 0
        self.num_rows = self.raw_data.shape[0]
        self.passNode = []
        for i in range(self.rows*self.columns):
            if i-self.cntPassNode <self.num_rows:
                if i+1 != self.raw_data[i-self.cntPassNode][0] and self.cntPassNode<(self.rows*self.columns-self.num_rows):
                    self.passNode.append(i+1)
                    self.cntPassNode += 1
                    # print(i)
            else :
                self.passNode.append(i+1)
                self.cntPassNode += 1
                # print(i)
        self.passNode.append(-1)
        # print(self.passNode)
        self.cntPassNode = 0
        self.cnt = 0
        self.nd_dict = dict()
        self.endNodes = []
        self.endNodesDistance = dict()
        self.startPoint = 1
        self.visited = []
        self.points = []
        self.initialTime , self.straightTime , self.turnTime , self.backTime = (float(1.18) , float(1.36) , float(1.34) , float(1.18))
        self.totalTimes = 20
        self.timesLeft = 20
        self.reset = False
        self.alreadyReset = False
        for i in range (self.rows*self.columns) :
            if i+1 == self.passNode[self.cntPassNode]:# or self.cntPassNode == len(self.passNode):
                self.cntPassNode+=1
                print(i , self.cntPassNode )
                continue
            print(i , self.cntPassNode , i+1)
            tmpNode = node.Node(self.raw_data , self.cntPassNode , i+1)
            if tmpNode.isEnd:
                self.endNodes.append(i+1)
                self.endNodesDistance[i+1] = self.setDistance(i+1)
            self.nd_dict[i+1] = tmpNode

    def resetTimesLeft(self):
        self.timesLeft = self.totalTimes
        return

    def checkIfReset(self):
        if self.reset == True:
            self.reset = False
            self.alreadyReset = True
            return True
        else:
            return False

    def getBackTime(self):
        return self.backTime

    def setDistance(self , index):
        
        # print(int((index-self.startPoint)/rows) , int((index-self.startPoint)%rows))
        # print(30*(int((index-self.startPoint)/rows)+int((index-self.startPoint)%rows)))
        return 30*(int((index-self.startPoint)/self.rows)+int((index-self.startPoint)%self.rows))

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

    def setPoints(self):
        for endNode in self.endNodes:
            return

    def setStartPoint(self , index):
        self.startPoint = index
        return

    def strategy_0(self, nd):
        return self.BFS(nd)

    def strategy_1(self , start):
        return self.Dijkstra(start)

    def strategy_2(self ,  start) :
        return self.Dijkstra_2(start)

    def strategy_3(self , start) :
        if self.alreadyReset:
            # print("using Dijkstra_1")
            return self.Dijkstra(start)
        else :
            # print("using Dijkstra_2")
            return self.Dijkstra_2(start)

    def get_Direction(self , directions) :
        lst = []
        for dir in directions :
            if dir == 0:
                lst.append('1')
            elif dir == 1:
                lst.append('2')
            elif dir == 2:
                lst.append('3')
            elif dir == 3:
                lst.append('4')
        return lst
            
    def inEndNodes(self , nodeIndex) :
        for endNode in self.endNodes :
            if endNode==nodeIndex :
                return True
        return False

    def inPassNodes(self , index) :
        for passNode in self.passNode:
            if passNode == index :
                return  True
        return False

    def timeAllLonger(self , queue , time) :
        for node in queue:
            if self.inEndNodes(node[0]):
                if(node[1]<=time):
                    return False
        return True

    def bestRoute(self , candidates):
        points = -1
        turns = 10E6
        bestEnd = -1
        # print(candidates)
        for candidate in candidates:
            # print(self.endNodesDistance[candidate[0]])
            if self.endNodesDistance[candidate[0]]>points:
                points = self.endNodesDistance[candidate[0]]
                turns = candidate[1]
                bestEnd = candidate[0]
            elif self.endNodesDistance[candidate[0]]==points:
                if candidate[1]<turns :
                    turns = candidate[1]
                    bestEnd = candidate[0]
        # print(bestEnd)
        return bestEnd

    def bestEfficiency(self , candidates):
        points = -1
        efficiency = -1
        turns = 10E6
        bestEnd = -1
        timesBest = -1
        timesLeast = 10E6
        returnTimesLeast = True
        # print(candidates)
        for candidate in candidates :
            time = candidate[1]
            if time < self.timesLeft:
                returnTimesLeast= False
                break

        for candidate in candidates:
            point , time , turn = self.endNodesDistance[candidate[0]] , candidate[1] , candidate[2]
            if returnTimesLeast:
                if time<timesLeast:
                    efficiency = float(point/time)
                    points = point
                    turns = turn
                    bestEnd = candidate[0]
                    timesLeast = time
                    timesBest = time
            else :
                # print("index " , candidate[0] , ": " , point ," , " , time , " , " , float(point/time))
                if float(point/time) > efficiency:
                    efficiency = float(point/time)
                    points = point
                    turns = turn
                    bestEnd = candidate[0]
                    timesBest = time
                elif float(point/time) == efficiency:
                    if point > points :
                        points = point
                        turns = turn
                        bestEnd = candidate[0]
                        timesBest = time
                    elif point == points:
                        if turn < turns :
                            turns = turn
                            bestEnd = candidate[0]
                            timesBest = time
        # print("----------------------------------------------")
        # print(points , efficiency , turns , bestEnd)    
        self.timesLeft -= timesBest 
        self.timesLeft += self.straightTime
        if self.timesLeft<0: 
            self.reset = True
        return bestEnd

    def setQueue(self , startIndex):
        queue = []
        for i in range(self.num_rows+self.cntPassNode):
            if self.inPassNodes(i+1):
                continue
            if (i+1) == startIndex:
                queue.append([i+1 , 0 , -1 , -1 , 0][:]) #index , timeTaken , parent , direction , turns
            else:
                already_visited = False
                for visited in self.visited:
                    if (i+1) == visited :  
                        already_visited = True
                        break
                if not already_visited :
                    queue.append([i+1 , 10E6 , -1 , -1 , 10E6][:])
        return queue

    def findRoute(self , queue):
        shortest , timeTaken , turns = self.chooseShortest(queue)
        queue.remove(shortest)
        tmpNode = self.nd_dict[shortest[0]]
        sucessors = tmpNode.getSuccessors()

        for suc in sucessors:
            queue = self.updateQueue(queue , suc , shortest)
            
        return queue , shortest , timeTaken , turns

    def chooseShortest(self , queue):
        # print("---------------------------------------------")
        # for q in queue:
        #     print(q)
        timeTaken , turns = 10E6 , 10E6
        shortest = []
        for list in queue :
            if list[1]<timeTaken:
                shortest = list
                timeTaken = list[1]
                turns = list[4]
            elif list[1]==timeTaken:
                if list[4]<turns:
                    shortest = list
                    turns = list[4]
        # print(shortest)
        return shortest , timeTaken , turns
 
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
        if (dir1==dir2 or dir1 == -1):
            return 0
        elif (dir1!=dir2) :
            return 1

    def nextStep(self , dist , dir1 , dir2):
        if (dir1==dir2 or dir1 == -1):
            return (dist/3)*self.straightTime #straight
        elif (dir1-dir2==2 or dir1-dir2==-2) :
            return self.backTime #back
        else:
            return (((dist/3)-1)*self.straightTime + self.turnTime) #left/right turn

    def updateQueue(self , queue , suc , shortest):
        pos=-1
        for i in range(len(queue)):
            if queue[i][0]==int(suc[0]) :
                pos = i
                break
        nextMoveTime = self.nextStep(suc[2] , shortest[3] , suc[1])
        # if pos!=-1 : print(shortest[0] , suc[0] , nextMoveTime)
        if pos!=-1 and (shortest[1] + nextMoveTime  < queue[ pos ][1]):
            queue[ pos ][1] = shortest[1] + nextMoveTime
            queue[ pos ][2] = shortest[0]
            queue[ pos ][3] = suc[1]
            queue[ pos ][4] = shortest[4] + self.TurnOrNot(shortest[3] , suc[1])
        elif pos!=-1 and (shortest[1] + nextMoveTime  == queue[ pos ][1]):
            if shortest[4] + self.TurnOrNot(shortest[3] , suc[1]) < queue[ pos ][4] : 
                queue[ pos ][2] = shortest[0]
                queue[ pos ][3] = suc[1]
                queue[ pos ][4] = shortest[4] + self.TurnOrNot(shortest[3] , suc[1])
        return queue
 
    def Dijkstra(self , start) :
        queue = self.setQueue(start) #將所有node塞入queue中
        records = []
        candidates = []
        while len(queue)!=0 :
            queue , shortest , timeTaken , turns = self.findRoute(queue) #找出下一個timeTaken最短的是誰，並且更新此node的successor

            records.append(shortest[:])
            if self.inEndNodes(shortest[0]) : #判斷是否是端點
                candidates.append([shortest[0] ,shortest[1] , turns][:]) #將端點塞進candidates中
                if self.timeAllLonger(queue , timeTaken): #判斷queue中還有沒有人的timeTaken與此node相同(True:沒有,False:有)
                    bestEnd = self.bestEfficiency(candidates) #找出效率最高的node
                    self.endNodes.remove(bestEnd)
                    self.visited.append(bestEnd)
                    return bestEnd , records

    def BFS(self, nd_from, nd_to):
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

    def Dijkstra_2(self , start) :
        queue = self.setQueue(start) #將所有node塞入queue中
        records = []
        candidates = []
        while len(queue)!=0 :
            queue , shortest , timeTaken , turns = self.findRoute(queue) #找出下一個timeTaken最短的是誰，並且更新此node的successor

            records.append(shortest[:])
            if self.inEndNodes(shortest[0]) : #判斷是否是端點
                candidates.append([shortest[0] , shortest[1], turns][:]) #將端點塞進candidates中
        # print(shortest[:])
        bestEnd = self.bestEfficiency(candidates) #找出效率最高的node
        self.endNodes.remove(bestEnd)
        self.visited.append(bestEnd)
        return bestEnd , records

    