import copy
import threading
import queue
import time
from datetime import datetime, timedelta
start_time = datetime.now()

list_of_threads = []  # contains all threads of routers
list_routers = []  # contains all routers
adj_list = {}  # adjacency list
router_queues = {}  # queue for each router
lock = threading.Lock()  # thread lock for printing
ans_table = {}
# process for each router


def lsr(router_id):
    # adj list of the router that stores its topology of the graph
    adj_list_router = {}
    # iteration info of the topology, ttl and the source
    adj_list_router["itr"] = 0
    adj_list_router["ttl"] = timedelta(minutes=30)
    adj_list_router["src"] = router_id
    router_time = datetime.now()
    # initialise adjlist
    for x in list_routers:
        adj_list_router[x] = {}
    # fill adjacentcy list with neighbours
    for x in adj_list[router_id]:
        adj_list_router[router_id][x] = adj_list[router_id][x]
        adj_list_router[x][router_id] = adj_list_router[router_id][x]
    # send this info, basically anouncing that I am this node and these are my neighbours
    for x in adj_list[router_id]:
        try:
            router_queues[x].put_nowait(copy.deepcopy(adj_list_router))
        except:
            print(x, "router's queue was full")
    while (True):
        # reset iteration according to tll
        if (router_time-datetime.now() > adj_list_router["ttl"]):
            router_time = datetime.now()
            adj_list_router["itr"] = 0
        # boolean to break loop
        breaker = 1
        # if all routers are empty all graphs have coverged
        for x in router_queues:
            if (not router_queues[x].empty()):
                breaker = 0
                break
        # break the loop if all queues are empty
        if (breaker):
            break
        # while queue is not empty
        while (not router_queues[router_id].empty()):
            # fetch some information
            shared_adj_list = router_queues[router_id].get()
            change = 0
            # check if there is info, if something is changed, set change to 1
            for x in shared_adj_list:
                if (not x == "itr" and not x == "src" and not x == "ttl"):
                    for y in shared_adj_list[x]:
                        if (y == "itr"):
                            continue
                        if (y not in adj_list_router[x]):
                            change = 1
                        adj_list_router[x][y] = shared_adj_list[x][y]
                        adj_list_router[y][x] = shared_adj_list[x][y]
            # if changed, then apply djikstra and send same info to neighbours(flooding)
            if (change):
                # increase iteration
                adj_list_router["itr"] += 1
                router_time = datetime.now()
                # send info to neighbours
                for x in adj_list[router_id]:
                    try:
                        router_queues[x].put_nowait(
                            copy.deepcopy(shared_adj_list))
                    except:
                        print(x, "router's queue was full")
                # djikstra
                # queue for djikstra
                queue_for_sp = queue.Queue(len(list_routers))
                # routing table
                routing_table = {}
                # initialise routing table
                for x in list_routers:
                    routing_table[x] = [-1, -1]
                routing_table[router_id] = [router_id, 0]
                queue_for_sp.put_nowait(router_id)
                # while queue is not empty
                while (not queue_for_sp.empty()):
                    # take a node
                    curr = queue_for_sp.get()
                    # for all edges of the node
                    for x in adj_list_router[curr]:
                        if (x == "itr"):
                            continue
                        # update if node can reaach in better distance and add it to queue
                        if (routing_table[x][1] == -1):
                            routing_table[x][1] = routing_table[curr][1] + \
                                adj_list_router[x][curr]
                            routing_table[x][0] = x
                            queue_for_sp.put_nowait(x)
                        elif (routing_table[x][1] > routing_table[curr][1]+adj_list_router[x][curr]):
                            routing_table[x][1] = routing_table[curr][1] + \
                                adj_list_router[x][curr]
                            routing_table[x][0] = curr
                            queue_for_sp.put_nowait(x)
                # save routing table in answer table
                ans_table[router_id] = routing_table
                # printing table, where info received , prints routing table and graph of this node, a bit hardcoded
                lock.acquire()
                print("Got table at", router_id, "from",
                      shared_adj_list["src"], "\nRouter was at iteration", adj_list_router["itr"]-1)
                print("_________________________")
                print("|\t\t\t|")
                s = "| Edges At "+router_id+"\t\t|"
                print(s)
                print("| Itr", adj_list_router["itr"], "\t\t|")
                print("|_______________________|", "\n|\t|\t|\t|")
                print("|", end=' ')
                print("From", "\t|",
                      "To", "\t|", "Cost", "\t|")
                print("|_______|_______|_______|")
                print("|\t|\t|\t|")
                for x in adj_list_router:
                    if (x == "itr" or x == "src" or x == "ttl"):
                        continue
                    for y in adj_list_router[x]:
                        if (y == "itr"):
                            continue
                        print("|", end=' ')
                        print(x, "\t|",
                              y, "\t|", adj_list_router[x][y], "\t|")
                print("|_______|_______|_______|")
                print("_________________________")
                print("|\t\t\t|")
                s = "| From "+router_id+"\t\t|"
                print(s)
                print("|_______________________|", "\n|\t|\t|\t|")
                print("|", end=' ')
                print("To", "\t|",
                      "Via", "\t|", "Cost", "\t|")
                print("|_______|_______|_______|")
                print("|\t|\t|\t|")
                for x in list_routers:
                    print("|", end=' ')
                    print(x, "\t|",
                          ans_table[router_id][x][0], "\t|", ans_table[router_id][x][1], "\t|")
                print("|_______|_______|_______|")
                lock.release()
            del shared_adj_list
        # sleep for info to arrive as queue would have been empty if we got here
        time.sleep(2)
    # djikstra in case graph was always complete in trivial cases
    # queue for djikstra
    queue_for_sp = queue.Queue(len(list_routers))
    # routing table
    routing_table = {}
    # initialise routing table
    for x in list_routers:
        routing_table[x] = [-1, -1]
    routing_table[router_id] = [router_id, 0]
    queue_for_sp.put_nowait(router_id)
    # while queue is not empty
    while (not queue_for_sp.empty()):
        # take a node
        curr = queue_for_sp.get()
        # for all edges of the node
        for x in adj_list_router[curr]:
            if (x == "itr"):
                continue
            # update if node can reaach in better distance and add it to queue
            if (routing_table[x][1] == -1):
                routing_table[x][1] = routing_table[curr][1] + \
                    adj_list_router[x][curr]
                routing_table[x][0] = x
                queue_for_sp.put_nowait(x)
            elif (routing_table[x][1] > routing_table[curr][1]+adj_list_router[x][curr]):
                routing_table[x][1] = routing_table[curr][1] + \
                    adj_list_router[x][curr]
                routing_table[x][0] = curr
                queue_for_sp.put_nowait(x)
    # save routing table in answer table
    ans_table[router_id] = routing_table


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
        router_queues[x] = queue.Queue(i*i*i)
    # start threads of each router
    for x in range(len(list_routers)):
        list_of_threads.append(threading.Thread(
            target=lsr, args=(list_routers[x],)))
        list_of_threads[x].start()
    # wait for all router threads to join before ending program
    for x in range(len(list_routers)):
        list_of_threads[x].join()
    # printing the routing tables of all the routers
    for router_id in ans_table:
        print("_________________________")
        print("|\t\t\t|")
        s = "| From "+router_id+"\t\t|"
        print(s)
        print("|_______________________|", "\n|\t|\t|\t|")
        print("|", end=' ')
        print("To", "\t|",
              "Via", "\t|", "Cost", "\t|")
        print("|_______|_______|_______|")
        print("|\t|\t|\t|")
        for x in list_routers:
            print("|", end=' ')
            print(x, "\t|",
                  ans_table[router_id][x][0], "\t|", ans_table[router_id][x][1], "\t|")
        print("|_______|_______|_______|")
    # This shall be the last lines of the code.
    end_time = datetime.now()
    print('Duration of Program Execution: {}'.format(end_time - start_time))


if __name__ == "__main__":
    main()
