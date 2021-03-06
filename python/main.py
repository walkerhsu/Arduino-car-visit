import node
import maze as mz
import BT
import score
import interface
import time
import serial
import threading

import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("data/3_3_maze(1).csv")
    #point = score.Scoreboard("data/UID.csv", "team_3")
    #interf = interface.interface()
    # TODO : Initialize necessary variables
    endNodes = maze.getEndNodes()
    s=''
    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        print("using method 3!!!!!!!!!!!!!!")
        startNode = maze.getStartPoint()
        startIndex = startNode.getIndex()
        print ("start from : " , startIndex)
        total_steps = 0
        while (len(endNodes)!=0) :
            endNode , lst = maze.strategy_3(startIndex)
            dist , m = maze.getHowToGo(startIndex , endNode ,lst)
            output1 = ''.join(m)
            dist -= maze.straightTime
            if startIndex == 1 :
                dist += maze.initialTime
                maze.timesLeft -= maze.initialTime
            total_steps += dist
            s+=output1
            print("from ",startIndex,"to ",endNode , " , taking ",dist," seconds , and gets ",maze.endNodesDistance[endNode]," points.")
            if maze.checkIfReset():
                print("     exceeds ",maze.timesLeft*(-1)," seconds at node " , endNode , "!!!")
                print("     time reseting...")
                maze.resetTimesLeft()
            elif maze.alreadyReset :
                print("")
            else:
                print("     ", maze.timesLeft , " seconds left !!!")
            
            if len(endNodes)!=0:
                print("backTurn at  ",endNode," , taking ",maze.getBackTime() , " seconds.")
                total_steps += maze.getBackTime()
                maze.timesLeft -= maze.getBackTime()
            
            startIndex = endNode
        print("string s = " , s)
        print("total seconds = ", total_steps)
        bt.SerialWrite(s)
        while True:
            msgWrite = input()
            if msgWrite == "exit": sys.exit()
            bt.SerialWrite(msgWrite)
    # elif (sys.argv[1] == '1'):
        # print("Mode 1: Self-testing mode.")
        # startNode = maze.getStartPoint()
        # startIndex = startNode.getIndex()
        # print ("start from : " , startIndex)
        # while(len(endNodes)!=0) :
        #     destination , directionPath= maze.strategy(startIndex)
        #     m = maze.get_Direction(directionPath)
        #     output1 = ''.join(m)
        #     #print(test1 , output1)
        #     s+=output1
        #     print("from ",startIndex,"to ",destination)
        #     startIndex = destination
            
        # print("string = " , s)
        # bt.SerialWrite(s)
        # while True:
        #     msgWrite = input()
        #     if msgWrite == "exit": sys.exit()
        #     bt.SerialWrite(msgWrite)
        # ## TODO: You can write your code to test specific function.
    elif (sys.argv[1] == '2'):
        print("Mode 2: Self-testing mode.")
        print("using method 3!!!!!!!!!!!!!!")
        startNode = maze.getStartPoint()
        startIndex = startNode.getIndex()
        print ("start from : " , startIndex)
        total_steps = 0
        while (len(endNodes)!=0) :
            endNode , lst = maze.strategy_3(startIndex)
            dist , m = maze.getHowToGo(startIndex , endNode ,lst)
            output1 = ''.join(m)
            dist -= maze.straightTime
            if startIndex == 1 :
                dist += maze.initialTime
                maze.timesLeft -= maze.initialTime
            total_steps += dist
            s+=output1
            print("from ",startIndex,"to ",endNode , " , taking ",dist," seconds , and gets ",maze.endNodesDistance[endNode]," points.")
            if maze.checkIfReset():
                print("     exceeds ",maze.timesLeft*(-1)," seconds at node " , endNode , "!!!")
                print("     time reseting...")
                maze.resetTimesLeft()
            elif maze.alreadyReset :
                print("")
            else:
                print("     ", maze.timesLeft , " seconds left !!!")
            
            if len(endNodes)!=0:
                print("backTurn at  ",endNode," , taking ",maze.getBackTime() , " seconds.")
                total_steps += maze.getBackTime()
                maze.timesLeft -= maze.getBackTime()
            
            startIndex = endNode
        print("string s = " , s)
        print("total seconds = ", total_steps)
        bt.SerialWrite(s)
        while True:
            msgWrite = input()
            if msgWrite == "exit": sys.exit()
            bt.SerialWrite(msgWrite)
        #for endNode in endNodes :
    
def read():
    point = score.Scoreboard("data/UID.csv", "team_3")
    while True:
        if bt.waiting():
            UID = bt.SerialReadString()
            print(UID)
            point.add_UID(UID)
            point.getCurrentScore()



def write():
    while True:
        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        bt.SerialWrite(msgWrite + "\n")

if __name__ == '__main__':
    bt = BT.bluetooth("/dev/tty.038-SerialPort") 
    while not bt.is_open(): pass
    print("BT Connected!")

    readThread = threading.Thread(target=read)
    readThread.daemon = True
    readThread.start()

    main()

