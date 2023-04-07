#Simple producer and consumer
#Imports
import random
import threading
import multiprocessing
import logging
from threading import Thread
# from queue import Queue

import time
logging.basicConfig(format='%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

#Functions
def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info(f'{processname}\{threadname}: {msg}\n')

# constant giving the buffer size
N = 10

#Producer
class Producer(Thread) :
    flag = True
    item = 0

    def stop_producing(self):
        self.flag = False
        display('Stop producing')

    def run(self) :
        # run method contains the thread code
        display("Producer started producing")
        # item = 0
        while (self.flag) :
            # producer loop
            item = self.produce_item()        
            mon.insert(item)    #use Monitor to insert
            time.sleep( 2 )
        

    def  produce_item(self) :
        num = random.randint(0,N) + 1
        display(f'Producer produced item: {num}')
        return num

#Consumer
class Consumer(Thread) :
    flag_c = True
    def stop_consuming(self) :
        self.flag_c = False
        display('stop consuming')
    
    def run(self) :
        # run method contains the thread code
        display("Consumer started consuming")
        item = 0
        while (self.flag_c) :
            # consumer loop
            item = mon.remove()
            self.consume_item(item)
            time.sleep( 1 )
        
    
    def consume_item(self, item) :
        display(f'Consuming : {item}')

class Monitor(Thread) :
    # this is a monitor
    # counters and indices
    buffer = [0] * N
    count = 0
    lo = 0
    hi = 0

    # Producer sleeps when buffer is full otherwise puts in buffer       
    
    def insert(self, val) :
        if (self.count == N) :
            self.go_to_sleep()
        # if the buffer is full, go to sleep
        self.buffer[self.hi] = val
        # insert an item into the buffer
        self.hi = (self.hi + 1) % N
        # slot to place next item in
        self.count += 1
        # one more item in the buffer now
        if (self.count == 1) :
            self.notify()
                    
    # Consumer sleeps when buffer is empty otherwise takes from buffer     
    def  remove(self) :
        val = 0
        i = 0
        if (self.count == 0) :
            self.go_to_sleep()  
        # if the buffer is empty, go to sleep
        val = self.buffer[self.lo]
        i = self.lo
        # fetch an item from the buffer
        self.lo = (self.lo + 1) % N
        # slot to fetch next item from
        self.count -= 1
        # one few items in the buffer
        if (self.count == (N - 1)) :
            self.notify()
        # if producer was sleeping, wake it up
        return (val)
    
    # Function to make them sleep.
    def go_to_sleep(self) :
        time.sleep( 5 )
        # try :
        #     self.wait(10)
        # except :
        #     display('Exception is caught while going to sleep')

p = Producer()
# instantiate a new producer thread 
c = Consumer()
# instantiate a new consumer thread 
mon = Monitor()   
# instantiate a new monitor
p.start()
# start the producer thread 

c.start()
# start the consumer thread 

# p.join()
# display('Producer has finished')
# c.join()
# display('Consumer has finished')

# So that loop doesn't run forever
time.sleep( 5 )
# try :
#     p.sleep(2)
#     c.sleep(2)
# except :
#     display('Exception is caught while calling sleep func')

p.stop_producing()
c.stop_consuming()

display('Finished')