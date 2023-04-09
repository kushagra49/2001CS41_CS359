import copy
import threading
import queue
import time
from datetime import datetime
start_time = datetime.now()

list_of_threads = []
list_routers = []
adj_list = {}
router_queues = {}
lock = threading.Lock()


def dvr(router_id):
    routing_table = {}
    routing_table["itr"] = [router_id, 0]
    for x in list_routers:
        routing_table[x] = [-1, -1]
    routing_table[router_id] = [router_id, 0]
    for x in adj_list[router_id]:
        routing_table[x] = [x, adj_list[router_id][x]]
    while (routing_table["itr"][1] < len(list_routers)):
        lock.acquire()
        print("Routing table of", router_id,
              "at iteration", routing_table["itr"][1])
        for x in list_routers:
            print(x, routing_table[x][0], routing_table[x][1])
        lock.release()
        if (routing_table["itr"][1] == len(list_routers)-1):
            return
        time.sleep(0.1)
        for x in adj_list[router_id]:
            try:
                router_queues[x].put_nowait(copy.deepcopy(routing_table))
            except:
                print(x, "router's queue was full")
        time.sleep(2)
        while (not router_queues[router_id].full()):
            continue
        while (not router_queues[router_id].empty()):
            shared_table = router_queues[router_id].get()
            for x in list_routers:
                if (routing_table[x][1] == -1 and shared_table[x][1] != -1):
                    routing_table[x] = [shared_table["itr"][0], shared_table[x]
                                        [1]+adj_list[router_id][shared_table["itr"][0]]]
                elif (routing_table != -1 and shared_table[x][1] != -1):
                    if (routing_table[x][1] > shared_table[x][1]+adj_list[router_id][shared_table["itr"][0]]):
                        routing_table[x] = [shared_table["itr"][0], shared_table[x]
                                            [1]+adj_list[router_id][shared_table["itr"][0]]]
            del shared_table
        routing_table["itr"][1] += 1


def main():
    input_file = open("topology.txt", "r")
    input_lines = input_file.readlines()
    i = int(input_lines[0])
    fixed_names = input_lines[1]
    for x in range(i):
        list_routers.append(fixed_names[2*x])
        adj_list[fixed_names[2*x]] = {}
    idx = 2
    while (True):
        edge = input_lines[idx]
        if (edge == "EOF"):
            break
        adj_list[edge[0]][edge[2]] = int(edge[4])
        adj_list[edge[2]][edge[0]] = int(edge[4])
        idx = idx+1
    # for x in adj_list:
    #     for y in adj_list[x]:
    #         print(x,y,adj_list[x][y])
    for x in list_routers:
        router_queues[x] = queue.Queue(len(adj_list[x]))
    for x in range(len(list_routers)):
        list_of_threads.append(threading.Thread(
            target=dvr, args=(list_routers[x])))
        list_of_threads[x].start()
    for x in range(len(list_routers)):
        list_of_threads[x].join()
    # This shall be the last lines of the code.
    end_time = datetime.now()
    print('Duration of Program Execution: {}'.format(end_time - start_time))


if __name__ == "__main__":
    main()
