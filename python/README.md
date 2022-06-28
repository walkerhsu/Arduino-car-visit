We first turn the map info into some kinds of csv file.

Then , we use BFS (Dijkstra) to find the best route to finish the map.

Finally , we save the route that can finish the whole map and send this message to Arduino by Bluetooth.

In the tracking process , if we get the UID , we will send some message to a specific server.

## message 

the message is a string encoded by '0' , '1' , '2' , '3' .

'0' means moves toeard north

'1' means moves toward east

'2' means moves toward south

'3' means moves toeard west

like this : 

<img width="634" alt="截圖 2022-06-28 下午12 41 32" src="https://user-images.githubusercontent.com/83209083/176094455-25810384-d1aa-4e50-b2fe-8f3502c1184d.png">

## UID of a card 

There's a UID detector on the car

When detected , Arduino will pass the UID to python by Bluetooth in the form of a string

Then , we will send this string to a specific server and add the corresponding score to it

like this : 

<img width="570" alt="截圖 2022-06-28 下午12 59 29" src="https://user-images.githubusercontent.com/83209083/176096525-17e116fe-59c8-4829-bd42-e6d0b3193287.png">

