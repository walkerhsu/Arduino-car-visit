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
    maze = mz.Maze("data/medium_maze.csv")
    #point = score.Scoreboard("data/UID.csv", "team_3")
    #interf = interface.interface()
    # TODO : Initialize necessary variables
    endNodes = maze.getEndNodes()
    s=''
    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")

        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        
    elif (sys.argv[1] == '1'):
        print("Mode 1: Self-testing mode.")
        startNode = maze.getStartPoint()
        startIndex = startNode.getIndex()
        print ("start from : " , startIndex)
        while(len(endNodes)!=0) :
            destination , directionPath= maze.strategy(startIndex)
            m = maze.get_Direction(directionPath)
            output1 = ''.join(m)
            #print(test1 , output1)
            s+=output1
            print("from ",startIndex,"to ",destination)
            startIndex = destination
            
        print("string = " , s)
            # test1 , test2= maze.strategy(11)
            # m = maze.get_Direction(test2)
            # output1 = ''.join(m)
            # print(test1 , output1)

            # test1 , test2 = maze.strategy_2(7,9)
            # m = maze.get_Direction(test2)
            # output2 = ''.join(m)
            # print(output2)

            # test1 , test2 = maze.strategy_2(7,9)
            # m = maze.get_Direction(test2)
            # output2 = ''.join(m)
            # print(output2)


        bt.SerialWrite(s)
        while True:
            msgWrite = input()
            if msgWrite == "exit": sys.exit()
            bt.SerialWrite(msgWrite)
        ## TODO: You can write your code to test specific function.
    elif (sys.argv[1] == '2'):
        print("Mode 2: Self-testing mode.")
        startNode = maze.getStartPoint()
        startIndex = startNode.getIndex()
        print ("start from : " , startIndex)
        total_steps = 0
        while(len(endNodes)!=0) :
            endNode , lst = maze.Dijkstra(startIndex)
            dist , m = maze.getHowToGo(startIndex , endNode ,lst)
            output1 = ''.join(m)
            s+=output1
            print("from ",startIndex,"to ",endNode , " cost ",dist," steps.")
            total_steps += dist
            startIndex = endNode
        print("string s = " , s)
        print("total steps = ", total_steps)
        #for endNode in endNodes :
    
def read():
    point = score.Scoreboard("data/UID.csv", "team_3")
    while True:
        if bt.waiting():
            UID = bt.SerialReadString()
            print(UID)
            point.add_UID(UID)



def write():
    while True:
        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        bt.SerialWrite(msgWrite + "\n")

if __name__ == '__main__':
    # bt = BT.bluetooth("/dev/tty.042-SerialPort") 
    # while not bt.is_open(): pass
    # print("BT Connected!")

    # readThread = threading.Thread(target=read)
    # readThread.daemon = True
    # readThread.start()

    main()

