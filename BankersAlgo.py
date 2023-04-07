# Program a simulation of the banker’s algorithm. 
# Your program should cycle through each of the bank clients asking for a request and evaluating 
# whether it is safe or unsafe. Output a log of requests and decisions to a file.

import os
try: 
    processes = int(input("Number of processes : "))
    resources = int(input("Number of resources : "))
    available_resources = [int(i) for i in input("Available resources (separated by space) : ").split()][0:resources]
    print("\n-- Allocated resources for each process (separated by space) --")
    currently_allocated = [[int(i) for i in input(f"Process {j + 1} : ").split()][0:resources] for j in range(processes)]
    print("\n-- Required resources for each process (separated by space)--")
    max_need = [[int(i) for i in input(f"Process {j + 1} : ").split()][0:resources] for j in range(processes)]
    first = int(input(f"\nPlease enter the Process number you want to run first or 0 for a safe sequence sugestion : "))
    if first > processes:
        assert(1 == 0)
    print(f"Currently available resources : {available_resources}\n")
except:
    print('Invalid input. Please start again')
    os._exit(1)

running = [True] * processes
count = processes
order = []
def display_unsafe(i):
    print(f'Process {i+1} :\n\tRequires : {max_need[i]} \n\tAvailable : {available_resources}')
    print("The processes are in an unsafe state.")

def display_safe():
    print(f"\tThe process is in a safe state.\n")
    print(f"\nCurrently available resources : {available_resources}\n")

def display_executng(i):
    print(f'Process {i+1} Requires : {max_need[i]}')
    print(f"Process {i + 1} is executing...")

def run(i):
    if running[i]:
        executing = True
        for j in range(resources):
            if max_need[i][j] > available_resources[j]:
                executing = False
                break
        if executing:
            display_executng(i)
            running[i] = False        
            for j in range(resources):
                available_resources[j] += currently_allocated[i][j]
            display_safe()
            order.append(i+1)
            return True
    return False
try:
    safe = True
    if  first != 0:
        i = first - 1    
        safe = run(i)
        count -= 1     
        
    if safe:
        while count != 0:    
            safe = False
            for i in range(processes):
                if first != 0 and i == first-1:
                    continue
                if running[i]:
                    safe = run(i)
                    if safe:
                        count -= 1
                        break
            if not safe and i != first-1:
                display_unsafe(i)
                break
    else:
        display_unsafe(i)
    if len(order) == processes:
        print(f"Safe order to run processes : {order}")
        os._exit(1)
except:
    print("Something went wrong. Please try again")
    os._exit(1)
