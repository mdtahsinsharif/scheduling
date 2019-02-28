from xlrd import open_workbook 

def prepare_schedule(load_sch, run, not_run, capacity, id, total_time):
    sch = []
    cur = 0
    load = 0
    i = 0
    mode = ""
    hor = []
    t = 0
    lst = []
    for row in range(total_time):
        lst1 = []
        for col in range(len(not_run)):
            lst1.append(0)
        lst.append(lst1)
            
    ## Time 0
    
    
    cost = 0
    while True:
        t = t+1
        if i>=len(load_sch):
            break;
        load = load_sch[i]
        i = i+1; ##for getting the load req
        if cur<load:
            mode = "INCREASING"
        elif cur>load:
            mode = "DECREASING"
        else:
            mode = "LEVEL"
        
        if mode == "INCREASING":
            while cur<load:
                if len(not_run)>0:
                    temp = not_run.pop(0)
                    cur += capacity[id[temp]]
                    cost += temp
                    run.append(temp)
                else:
                    print "Cannot meet load"
                    t = total_time+1 ##indicator that you should quit
                    break;
        elif mode == "DECREASING":
            if load <= 0:
                while len(run)>0:
                    temp = run.pop(len(run)-1)
                    not_run.append(temp)
                    cur = 0
                cost = 0
            else:
                while cur>=load:
                    temp = run.pop(len(run)-1)
                    cur -= capacity[id[temp]]
                    cost -= temp
                    not_run.append(temp)
                t1 = not_run.pop(len(not_run)-1)
                cur += capacity[id[t1]]
                run.append(t1)
                cost += t1
        
        if t>=len(lst) or t>=total_time:
            break
        
        for j in range(len(run)):
            lst[t][id[run[j]]-1] = 1
        for k in range(len(not_run)):
            lst[t][id[not_run[k]]-1] = 0
        
        
            
        run.sort()
        not_run.sort()

        print "t =",t
        print "load: ", load
        print "current capacity: ", cur 
        print "current cost: ", cost 
        print "running: ",
        for qw in run:
            print id[qw],
        print " " 
        print "not running: ",
        for wq in not_run:
            print id[wq],
        print " "
        print " "
    return lst


generators_capacities_given = [20,76,20,76,100,100,197,197,12,155,155,400,400,50,155,350];
generator_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
generators_cost = [28.967,18.433,28.947,18.403,17.5904,17.6004,17.1925,17.2125,29.453,23.8096,23.8196,6.960789,6.970789,28.313,23.8296,26.2131]
generator_id_map = {}
for ii in range(len(generators_cost)):
    generator_id_map[generators_cost[ii]] = generator_ids[ii];
    


generators_capacity = {}
load_schedule = [1206,1134,1080,1062,1062,1080,1332,1548,1710,1728,1728,1710,1710,1710,1674,1692,1782,1800,1800,1728,1638,1494,1413,1134];
prev = 0;



print "Length of gen cost: ", len(generators_cost)
print "Length of gen capacities: ", len(generators_capacities_given)

for i in range(len(generators_cost)):
    cost1 = generators_cost[i]
    id1 = generator_id_map[cost1]
    cap1 = generators_capacities_given[i];
    generators_capacity[id1] = cap1;

generators_cost.sort()

running = []
not_running = generators_cost[:]

total_time = 25
schedule = prepare_schedule(load_schedule, running, not_running, generators_capacity, generator_id_map, total_time)
for x in schedule:
    print x

        