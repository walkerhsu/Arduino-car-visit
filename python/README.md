We first turn the map info into some kinds of csv file.

Then , we use BFS (Dijkstra) to find the best route to finish the map.

Finally , we save the route that can finish the whole map and send this message to Arduino by Bluetooth.

#message 

the message is a string encoded by '0' , '1' , '2' , '3' .

'0' means moves toeard north

'1' means moves toward east

'2' means moves toward south

'3' means moves toeard west



