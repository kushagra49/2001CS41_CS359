import copy
import threading
import queue
import time
from datetime import datetime
start_time = datetime.now()

list_of_threads = []  # contains all threads of routers
list_routers = []  # contains all routers
adj_list = {}  # adjacency list
router_queues = {}  # queue for each router
lock = threading.Lock()  # thread lock for printing

# process for each router


def dvr(router_id):
    # dict for routing table
    routing_table = {}
    # defingin table's id and iteration
    routing_table["itr"] = [router_id, 0]
    # add all routers to the table
    for x in list_routers:
        routing_table[x] = [-1, -1]
    # setting distance and next neighbour for the router itself
    routing_table[router_id] = [router_id, 0]
    # initialising routing table according to adjacency list
    for x in adj_list[router_id]:
        routing_table[x] = [x, adj_list[router_id][x]]
    # to track for changes
    changes = {}
    for x in list_routers:
        changes[x] = 0
    # number of iterations = n-1 for n routers
    while (routing_table["itr"][1] < len(list_routers)):
        # lock for printing
        lock.acquire()
        # printing, a bit hard coded to create table
        print("_________________________")
        print("|\t|\t\t|")
        s = "| "+router_id+"\t| iteration "+str(routing_table["itr"][1])+"\t|"
        print(s)
        print("|_______|_______________|", "\n|\t|\t|\t|")
        print("|", end=' ')
        print("To", "\t|",
              "Via", "\t|", "Cost", "\t|")
        print("|_______|_______|_______|")
        print("|\t|\t|\t|")
        for x in list_routers:
            print("|", end=' ')
            if (changes[x]):
                print("*", end='')
            print(x, "\t|",
                  routing_table[x][0], "\t|", routing_table[x][1], "\t|")
        print("|_______|_______|_______|")
        lock.release()
        # release lock after printing
        # reset changes to 0 after printing
        for x in list_routers:
            changes[x] = 0
        # no need to proceed if on last iteration
        if (routing_table["itr"][1] == len(list_routers)-1):
            return
        # sleep to allow everyone to process previous info and print
        time.sleep(0.1)
        # put copy of routing table in neighbours queue
        for x in adj_list[router_id]:
            try:
                router_queues[x].put_nowait(copy.deepcopy(routing_table))
            except:
                print(x, "router's queue was full")
        # sleep after putting copy, so that all others can finish the same action
        time.sleep(2)
        # while loop to wait for queue to be full, i.e. wait for info from all neighbours
        while (not router_queues[router_id].full()):
            continue
        # till queue is not empty remove tables from current routers queue
        while (not router_queues[router_id].empty()):
            shared_table = router_queues[router_id].get()
            for x in list_routers:
                # if we cant reach a node but some neigbour can
                if (routing_table[x][1] == -1 and shared_table[x][1] != -1):
                    routing_table[x] = [shared_table["itr"][0], shared_table[x]
                                        [1]+adj_list[router_id][shared_table["itr"][0]]]
                    changes[x] = 1
                # if we find a shorter way to reach some node
                elif (routing_table != -1 and shared_table[x][1] != -1):
                    if (routing_table[x][1] > shared_table[x][1]+adj_list[router_id][shared_table["itr"][0]]):
                        routing_table[x] = [shared_table["itr"][0], shared_table[x]
                                            [1]+adj_list[router_id][shared_table["itr"][0]]]
                        changes[x] = 1
            del shared_table
        # increment iteration
        routing_table["itr"][1] += 1


def main():
    # handle input from file
    input_file = open("topology.txt", "r")
    input_lines = input_file.readlines()
    i = int(input_lines[0])
    fixed_names = input_lines[1]
    # split line containing all routers based on blank space
    fixed_names = fixed_names.split(' ')
    # last splited node on line may contain \n
    temp = fixed_names[i-1].split('\n')
    fixed_names[i-1] = temp[0]
    # add all nodes to adjacency list dict
    for x in range(i):
        list_routers.append(fixed_names[x])
        adj_list[fixed_names[x]] = {}
    idx = 2
    # take all edges, and add them to adjacency list
    while (True):
        edge = input_lines[idx]
        if (edge == "EOF"):
            break
        edge = edge.split(" ")
        adj_list[edge[0]][edge[1]] = int(edge[2])
        adj_list[edge[1]][edge[0]] = int(edge[2])
        idx = idx+1
    # create queue for each router
    for x in list_routers:
        router_queues[x] = queue.Queue(len(adj_list[x]))
    # start threads of each router
    for x in range(len(list_routers)):
        list_of_threads.append(threading.Thread(
            target=dvr, args=(list_routers[x],)))
        list_of_threads[x].start()
    # wait for all router threads to join before ending program
    for x in range(len(list_routers)):
        list_of_threads[x].join()
    # This shall be the last lines of the code.
    end_time = datetime.now()
    print('Duration of Program Execution: {}'.format(end_time - start_time))


if __name__ == "__main__":
    main()
