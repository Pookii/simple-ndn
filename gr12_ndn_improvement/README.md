## This code can be run on the pi to complete the demonstration of ndn network routing as exemplified in the report

* In this demo, each pi has a network, there is a router and several devices in each network.

* pi25 connects with pi43 and pi44, pi44 connects with pi 45. 

* In the .log file named for each router you can see how the fib is created and how the data is routed according to the fib, and in the console output you can see whether the data comes from the producer or the router's content store

### step:
0. upload code to macneill.scss.tcd.ie machine
1. login in rasp-025.berry.scss.tcd.ie
    * cd gr12_ndn_improvement
    * sh ./start_router_pi25.sh
2. login in rasp-043.berry.scss.tcd.ie
    * cd gr12_ndn_improvement
    * sh ./start_router_pi43.sh
3. login in rasp-044.berry.scss.tcd.ie
    * cd gr12_ndn_improvement
    * sh ./start_router_pi44.sh
4. login in rasp-045.berry.scss.tcd.ie
    * cd gr12_ndn_improvement
    * sh ./start_router_pi45.sh
5. on rasp-043.berry.scss.tcd.ie
    * sh ./start_producer_pi43.sh
6. on rasp-045.berry.scss.tcd.ie, send a interest packet "/area43/device1/speed/1.txt" by using this command, then you can see the data packet from /area43/device1 in the output
    * sh ./start_consumer_pi45.sh
  
7. on rasp-044.berry.scss.tcd.ie, send same interest packet "/area43/device1/speed/1.txt" by using this command, then you can see the data packet from area44 in the output, because In the previous pi45 request, the packet was routed to the pi44 router, which added it to its content store before forwarding it.
   * sh ./start_consumer_pi44.sh






