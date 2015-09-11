// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-

/*

  SpinnIO Test program to send spikes
  to SpiNNaker using the EIEIO protocol 
  suitable for use with the SpiNNaker example
  script spike_injection.py

*/



#include <EIEIOSender.h>

#include <stdio.h>
#include <string>
#include <time.h>
#include <unistd.h>

using namespace std;
using namespace spinnio;


int main(int argc, char *argv[]) 
{
    
    int spinn_port = 12346;
    string spinn_ip = "192.168.1.1";
    string db = "/home/ubuntu/spinn103/examples/application_generated_data_files/latest/input_output_database.db";

    // Create the sender (creates socket and does toolchain handshake)
    // The port can actually be anything
    // the IP should be the SpiNNaker board IP
    // the database path is the path to the database created by the toolchain
    // for whatever network is being run

    EIEIOSender *mySender = new EIEIOSender(spinn_port,(char*)spinn_ip.c_str(), true, (char*)db.c_str());


    // start the sender thread
    mySender->start();

    int neuronID = 25;
    int stepsToRun = 25;
    int count = 0;

    // Add spikes to send queue
    // this should create two packets
    // with 63 spikes and one with 20
    for (int s=0; s < 146; s++){

       mySender->addSpikeToSendQueue(s);
       if (neuronID == 25){
        neuronID = 40;
       }else{
        neuronID = 25;
       }

    }
    // enable the queue for processing

    mySender->enableSendQueue();  

    // run for the number of steps defined above
    while(count < stepsToRun){
      int sendSize = mySender->getSendQueueSize();

      // continue to add new spikes to the send queue
      mySender->addSpikeToSendQueue(neuronID);
      if (neuronID == 25){
       neuronID = 40;
      }else{
       neuronID = 25;
      }

      // wait here 

      usleep(1000000);

      count++;

    } // main processing loop

    printf("Finished, cleaning up.....\n");

    // clean up

    // close socket

    mySender->closeSendSocket();

    // nullify sender object
    
    mySender = NULL;

}



