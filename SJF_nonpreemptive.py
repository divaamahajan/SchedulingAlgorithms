# Programming Questions 
# 1. (50) Implement a program for SJF(non-preemptive) scheduling. Given n processes with their burst times and Arrival Time, the task is to find average waiting time and average turn around time and completion time using SJF scheduling algorithm. 
# • Completion Time: Time at which process completes its execution. 
# • Turn Around Time: Time Difference between completion time and arrival time. Turn Around Time = Completion Time – Arrival Time 
# • Waiting Time: Time Difference between turn around time and burst time. Waiting Time = Turn Around Time – Burst Time

def pop_ready(ready_queue, start_time):
    # sort the ready queue processes  based on burst time
    ready_queue.sort(key=lambda x:x[2])
    p = ready_queue[0] # first process in the queue
    arrival_time = int(p[1])
    burst_time = int(p[2])
    completion_time = start_time + burst_time 
    turn_around_time = completion_time - arrival_time
    waiting_time = turn_around_time - burst_time
    idx = p[7] # index in the original queue
    process[idx][3] = completion_time
    process[idx][4] = turn_around_time
    process[idx][5] = waiting_time
    process[idx][6] = False #completed
    ready_queue.pop(0) #remove the process from the queue
    start_time = completion_time
    return start_time

n = 0
process = []
ans = ''
while ans != 'Q':
    n += 1
    process.append([n] + input(f'Please enter the Arrival Time and Burst time (separated by space) for Process{n} \n').split() + [0,0,0,True])
    ans = input('Press "Q" to Quit and proceed with calculations or any other key to add more processes\n').upper()


#Sort Arrival
process.sort(key=lambda x:x[1])
ready_queue = []
start_time = int(process[0][1]) #first process' arrival time

j=0
while j < n: #scan each process in the process queue
    for i in range(j,n+1): # Check for all the  process to be added to the ready queue
        if i == n: # a check added to maintain index of main process queue
            break
        arrival_time = int(process[i][1])
        yet_to_execute = process[i][6]
        if arrival_time <= start_time:
            if yet_to_execute:
                #add to the ready queue
                ready_queue.append(process[i] + [i]) #index i in the original queue saved for updates
        else:
            break #since sorted by arrival
    j = i #start from processes not yet scanned to be added to ready queue

    #calculations and execution of a process in ready queue    
    start_time = pop_ready(ready_queue, start_time )

#If the ready queue still has processes
while ready_queue:
    start_time = pop_ready(ready_queue , start_time)
avg_waiting = 0
avg_tot = 0    
for pid in process:
    print(f"ProcessID : P{pid[0]}")
    print(f"\tArrival Time  : {pid[1]}")
    print(f"\tBurst Time    : {pid[2]}")
    print(f"\tCompletion Time: {pid[3]}")
    print(f"\tTurnAround Time: {pid[4]}")
    avg_tot += pid[4]
    print(f"\tWaiting Time   : {pid[5]}\n")
    avg_waiting += pid[5]

print(f"Average Waiting Time    : {avg_waiting/n}")
print(f"Average TurnAround Time : {avg_tot/n}")