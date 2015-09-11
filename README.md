Information about the SpinnIO test program
-----------------------------------------------

This folder contains some simple programs to 
test the basic functionality of the SpinnIO
library

spinnioSendOnly.cpp - sets up a spike sender. 
spinnioRecvOnly.cpp - sets up a spike receiver.
spinnioSendRecv.cpp - sets up a spike receiver and sender.


Compiling the programs
----------------------

1. You will likely need to change some information in these
   programs to reflect your SpiNNaker IP and the path
   to the database.

2. do ccmake ./ 

2. cmake will ask for the paths to SpinnIO
   cmake config file this should be ${HOME}/SpinnIO
   unless you have installed elsewhere

3. do make and then run the executables

4. example PyNN scripts for send, receive and
   send-receive are in the examples directory 

