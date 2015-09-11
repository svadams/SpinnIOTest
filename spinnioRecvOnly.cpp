// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

/*

  SpinnIO Test program to receive spikes
  from SpiNNaker using the EIEIO protocol 
  suitable for use with the SpiNNaker example
  script live_packet_output_synfire_chain.py

*/



#include <EIEIOReceiver.h>

#include <stdio.h>
#include <string>
#include <time.h>
#include <unistd.h>

using namespace std;
using namespace spinnio;


int main(int argc, char *argv[]) 
{
    
    int spinn_port = 17895;
    string spinn_ip = "192.168.1.1";
    string db = "/home/ubuntu/spinn103/examples/application_generated_data_files/latest/input_output_database.db";

    // Create the receiver (creates socket and does toolchain handshake)
    // The port needs to be whatever port is defined for SpiNNaker
    // in the central or user spynnaker.cfg
    // the IP should be the SpiNNaker board IP
    // the database path is the path to the database created by the toolchain
    // for whatever network is being run

    EIEIOReceiver *myReceiver = new EIEIOReceiver(spinn_port,(char*)spinn_ip.c_str(), true, (char*)db.c_str());


    // start the receiver thread
    myReceiver->start();


    int numSpikes = 0;
    int stepsToRun = 50;
    int count = 0;
 

    // run for the number of steps defined above
    while(count < stepsToRun){
      int recvSize = myReceiver->getRecvQueueSize();

      // If there are incoming packets in the receiver queue
      // then process them and increment count of spikes

      if (recvSize > 0){
         // get the next packet from the queue
         list<pair<int, int> > spikeEvents = myReceiver->getNextSpikePacket();
         // get the individual spikes from the packet
         for(list<pair<int, int> >::iterator iter = spikeEvents.begin();iter != spikeEvents.end(); ++iter) {
            pair<int,int> spikeEvent = *iter;
            printf("Time %d, ID %d\n", spikeEvent.first, spikeEvent.second);
            // erase (time, nrn id) pair from list
            iter = spikeEvents.erase(iter);
            numSpikes++;
         }
         printf("Total spikes recv %d recv queue size %d\n", numSpikes,recvSize);
      }

      // wait for 1 sec here 

      usleep(1000000);

      count++;

    } // main processing loop

    printf("Finished, cleaning up.....\n");

    // clean up

    // close socket

    myReceiver->closeRecvSocket();

    // nullify receiver object
    
    myReceiver = NULL;


}



