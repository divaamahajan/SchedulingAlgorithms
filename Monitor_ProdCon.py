#Simple producer and consumer
#Imports
import random
from subprocess import STD_OUTPUT_HANDLE
import threading
import multiprocessing
import logging
from threading import Thread
import os
import time
from tracemalloc import stop

# constant giving the buffer size
flag_invalid = True
Max = 100
while flag_invalid:
    N = input("Please enter the size of the buffer: ")
    if N.isdigit():
        N = int(N)
        flag_invalid = False

#logging function
logging.basicConfig(format='%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)
def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info(f'{processname}\{threadname}: {msg}\n')

#Producer
class Producer(Thread) :
    flag = True
    item = 0
    count_p = 0
    quit = ''
    
    def stop_producing(self):
        self.flag = False
        print(f'\nCount of Items Produced: {self.count_p} \nStop producing')

    def run(self) :
        # run method contains the thread code
        display("Producer started producing")
        try:
            while (self.flag) :
                # producer loop
                item_produced = self.produce_item()                        
                self.count_p += 1     
                self.quit = m.insert(item_produced, self.count_p)    #use Monitor to insert
                if self.quit == 'Q':
                    break
            self.timedout = True
            p.stop_producing()
            c.stop_consuming()
        except:
            self.timedout = True
            p.stop_producing()  
            c.stop_consuming()
    def  produce_item(self) :
        item_produced = random.randint(1,N) # just an item
        display(f'Producer produced item: {item_produced}')
        return item_produced

#Consumer
class Consumer(Thread) :
    flag_c = True
    count_c = 0
    # quit = ''
    def stop_consuming(self) :
        self.flag_c = False
        print(f'Count of Items Consumed: {self.count_c} \nStop consuming')
        os._exit(1)     

    def run(self) :
        # run method contains the thread code
        display("Consumer started consuming")
        item = 0
        try:            
            while (self.flag_c):
                # consumer loop
                item = m.remove(self)
                self.consume_item(item)
                self.count_c += 1
                if p.quit == 'Q':
                    break
            self.timedout = True
            p.stop_producing()
            c.stop_consuming()
        except:            
            self.timedout = True
            p.stop_producing()
            c.stop_consuming()

    def consume_item(self, item) :
        display(f'Consuming : {item}')

class Monitor() :
    # this is a monitor
    # counters and indices
    buffer = [0] * N
    count = lo = hi = 0
    quit = ''

    # Initialising a condition class object
    condition_obj = threading.Condition()

    # Producer sleeps when buffer is full otherwise puts in buffer           
    def insert(self, item, count_insert) :
        self.condition_obj.acquire()
        if (self.count == N) :
            self.go_to_sleep()          # if the buffer is full, go to sleep        
        self.buffer[self.hi] = item     # insert an item into the buffer
        self.hi = (self.hi + 1) % N     # slot to place next item in
        self.count += 1                 #inventory size
        print("INSERT inventory size = ", self.count)
        # one more item in the buffer now
        
        if count_insert % Max == 0:
            self.quit = input(f'Producer has produced {count_insert} items so far. press "Q" to quit or any other key to continue.').upper()
        if self.quit == 'Q':       
            self.condition_obj.notify()     
            p.stop_producing()
            c.stop_consuming()
        if (self.count == 1) :
            self.condition_obj.notify()
        return self.quit
                    
    # Consumer sleeps when buffer is empty otherwise takes from buffer     
    def  remove(self, consumer: Thread) :
        self.condition_obj.acquire()
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
            self.condition_obj.notify()
        # if producer was sleeping, wake it up
        print("REMOVE inventory size = ", self.count)
            # Releasig the lock after consuming
        return (val)
    
    # Function to make them sleep.
    def go_to_sleep(self) :
        # calling_thread.wait(10)
        self.condition_obj.wait(2)

    def release_locks(self):
        self.condition_obj.release()

p = Producer(daemon = True) # instantiate a new producer thread 
c = Consumer(daemon = True) # instantiate a new consumer thread 
m = Monitor()               # instantiate a new monitor 

p.start()               # start the producer thread 
c.start()               # start the consumer thread 

time.sleep(2)

p.join()    # display('Producer has finished')
c.join()    # display('Consumer has finished')

time.sleep(5)

p.stop_producing()
c.stop_consuming()

m.release_locks()
