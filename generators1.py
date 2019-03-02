import pandas as pd
import numpy as np
import time
import xlwt 
from xlwt import Workbook 

def update_capacity(cur_cap,ramp_up,id,addGen,capacity):
    if capacity[id[addGen]] <= ramp_up[id[addGen]]:
	return capacity[id[addGen]], capacity[id[addGen]]*addGen
    else:
	if ramp_up[id[addGen]]+cur_cap[id[addGen]] > capacity[id[addGen]]:
	    return capacity[id[addGen]], capacity[id[addGen]]*addGen
	else:
	    return ramp_up[id[addGen]]+cur_cap[id[addGen]], (ramp_up[id[addGen]]+cur_cap[id[addGen]])*addGen

def add_capacity_rampup(cap, ramp_up, ids, addGen):
    if cap[ids[addGen]] <= ramp_up[ids[addGen]]:
	return cap[ids[addGen]]
    else:
	return ramp_up[ids[addGen]]

def prepare_schedule(load_sch, run, not_run, capacity, id, total_time, ramp_up, ramp_down, all_gen_size):
    sch = []
    cur = 0
    load = 0
    i = 0
    mode = ""
    hor = []
    t = 0
    lst = []
    total_cost_return = 0
    for row in range(total_time+1):
        lst1 = []
        for col in range(len(not_run)):
            lst1.append(0)
        lst.append(lst1)
            
    ## Time 0
    
    cur_cap = {}
    cur_cap2 = {}
    cost = 0
    off = {}
    while True:
        t = t+1
	if t>total_time:
	    break;	
	cur = 0
	cost = 0
	##print run
	for gen in run:
	    cur_cap2[id[gen]], cost_ = update_capacity(cur_cap,ramp_up,id,gen,capacity)
	    cost += cost_
	    cur += cur_cap2[id[gen]] 
	##print "cur_cap2: ", cur_cap2
	##print "cur_cap: ", cur_cap
        cur_cap = {}
	cur_cap = cur_cap2.copy()
	cur_cap2 = {}
	
	for key,val in off.items():
	    for key,val in off.items():
		##print "Turning off id: ",key
		##print "list: ", lst
		lst[t][key-1] = 1	    
	    ##print "off is: ", off
	    if off[key] <= ramp_down[key]:
		for running_cost__, ids__ in id.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
		    if key == ids__:
			cost += (off[key])*(running_cost__)
			cur += off[key]
			del off[key]
	    else:
		for running_cost__, ids__ in id.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
		    if key == ids__:
			tmp = off[key]
			cost += (ramp_down[key])*(running_cost__)
			cur += ramp_down[key]
			off[key] = tmp - ramp_down[key]
		
		
	    
	##print "cur_cap2 after clearing: ", cur_cap2
	##print "cur_cap after copying: ", cur_cap	
        
	load = load_sch[i]

        i = i+1; ##for getting the load req
        
        
        if cur<load:
            mode = "INCREASING"
        elif cur>load:
            mode = "DECREASING"
        else:
            mode = "LEVEL"
        
        if mode == "INCREASING":
	    print " "
	    print "---Load was more than Current Load-----"
            while cur<load:
                if len(not_run)>0:
                    temp = not_run.pop(0)
                    ##cur += capacity[id[temp]]
		    cur_cap[id[temp]] = add_capacity_rampup(capacity, ramp_up, id, temp)
                    cur += cur_cap[id[temp]]
                    cost += cur_cap[id[temp]]*temp
                    run.append(temp)
                else:
                    print "Cannot meet load"
		    print "current req load: ", load
		    print "current produced: ", cur
                    ##t = t-1 ##indicator that you should quit
                    i = i-1
		    total_time = total_time + 1
		    lst11 = []
		    ##print lst
		    for col1 in range(all_gen_size):
			lst11.append(0)
		    lst.append(lst11)	
		    ##print lst
                    break;
        elif mode == "DECREASING":
	    print " "
	    print "---Load was less than Current Load-----"
            if load <= 0:
                while len(run)>0:
                    temp = run.pop(len(run)-1)
                    not_run.append(temp)
                    cur = 0
                cost = 0
            else:
		tmp = 0
		tmp_val = 0
                while cur>=load and len(run)>0:
		    ##print " load: ", load, "cur: ", cur
		    ##print "run :", run
		    ##print "not run: ", not_run
                    temp = run.pop(len(run)-1)
		    ##print "load: ", load
		    ##print "curr: ", cur
                    ##print temp
                    cur -= cur_cap[id[temp]]
		    cost -= temp*cur_cap[id[temp]]
		    if ramp_down[id[temp]] < cur_cap[id[temp]]:
			off[id[temp]] = cur_cap[id[temp]] - ramp_down[id[temp]]
			cur += cur_cap[id[temp]]
			cur -= ramp_down[id[temp]]
			cost += temp*cur_cap[id[temp]]
			cost -= temp*(ramp_down[id[temp]])
                    ##print off
		    tmp_key, tmp_val = id[temp], cur_cap[id[temp]]
		    del cur_cap[id[temp]]
                    not_run.append(temp)
                t1 = not_run.pop(len(not_run)-1)
		cur_cap[id[t1]] = tmp_val
                cur += capacity[id[t1]]
                run.append(t1)
                cost += t1*capacity[id[t1]]
        
        ##if t>total_time:
          ##  break
        
        for j in range(len(run)):
            lst[t][id[run[j]]-1] = 1
        for k in range(len(not_run)):
            lst[t][id[not_run[k]]-1] = 0
        
	for key,val in off.items():
	    #print "Turning on id: ", key
	    lst[t][key-1] = 1	            
            
        run.sort()
        not_run.sort()
	
	print " "
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
	total_cost_return += cost
    return lst, total_cost_return


#reading the csv and setting values to arrays for different coloumns 	
start_time = time.time()
instance = 10
csvCol = pd.read_csv('./data/gen_data_instance_' + str(instance) + '.csv')

csv_generators_capacities_given = csvCol['Capacity (MW)']
csv_generator_ids = csvCol['Generator Number']
csv_generators_cost = csvCol['Cost ($/MW)']
csv_load_schedule = csvCol['Load (MW)']
csv_ramp_up = csvCol['Ramp up (MW/h)']
csv_ramp_down = csvCol['Ramp down (MW/h)']


generators_capacities_given = []
generator_ids = []
generators_cost = []
load_schedule = []
ramp_up = []
ramp_down = []


#converting csv arrays to local lists

for i in csv_generators_capacities_given:
	if (np.isnan(i)):
		break
	generators_capacities_given.append(i)
	
for j in range(len(generators_capacities_given)):
	##print csv_generator_ids
	##if (np.isnan(j)):
	##	break
	generator_ids.append(int(j+1))
	
for k in csv_generators_cost:
	if (np.isnan(k)):
		break
	generators_cost.append(k)
	
for l in csv_load_schedule:
	if (np.isnan(l)):
		break
	load_schedule.append(l)
##print load_schedule
for m in csv_ramp_up:
	if (np.isnan(m)):
		break
	ramp_up.append(m)
	
for n in csv_ramp_down:
	if (np.isnan(n)):
		break
	ramp_down.append(n)
	
	
### --------------- DEBUG CODE -----------###	
#print generators_capacities_given
#print generator_ids
#print generators_cost
#print load_schedule
#print ramp_up
#print ramp_down
	
#generators_capacities_given = [20,76,20,76,100,100,197,197,12,155,155,400,400,50,155,350];
#generator_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#generators_cost = [28.967,18.433,28.947,18.403,17.5904,17.6004,17.1925,17.2125,29.453,23.8096,23.8196,6.960789,6.970789,28.313,23.8296,26.2131]
#load_schedule = [1206,1134,1080,1062,1062,1080,1332,1548,1710,1728,1728,1710,1710,1710,1674,1692,1782,1800,1800,1728,1638,1494,1413,1134];	
	
### ------------- END DEBUG CODE ----------###
	
	
generator_id_map = {}
for ii in range(len(generators_cost)):
    generator_id_map[generators_cost[ii]] = generator_ids[ii];

generator_rampup_map = {}
for ii in range(len(generators_cost)):
    generator_rampup_map[generator_id_map[generators_cost[ii]]] = ramp_up[ii]

generator_rampdown_map = {}
for ii in range(len(generators_cost)):
    generator_rampdown_map[generator_id_map[generators_cost[ii]]] = ramp_down[ii]

generators_capacity = {}
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
##print not_running
wb = Workbook() 
sheet1 = wb.add_sheet('Output_instance_' + str(instance)) 

total_time = len(load_schedule)
schedule, t_cost = prepare_schedule(load_schedule, running, not_running, generators_capacity, generator_id_map, total_time, generator_rampup_map, generator_rampdown_map, len(not_running))
ti = 0
print "   ",


for ty in range(len(generator_ids)):
    print str(generator_ids[ty]),
    sheet1.write(generator_ids[ty], 0, generator_ids[ty])
    print "",
print ""
ti = total_time+1 - len(schedule)
row_excel = 1
col = 0
for x in range(len(schedule)):
    if ti<0:
	sheet1.write(col,row_excel,str(ti))
	print str(ti),
    elif ti < 10:
	sheet1.write(col,row_excel,str(ti))
	print "0"+str(ti),
    else:
	sheet1.write(col,row_excel,str(ti))
	print str(ti),
    for y in range(len(schedule[x])):
	sheet1.write(y+1,row_excel,schedule[x][y])
	print schedule[x][y],"",
    print ""
    row_excel = row_excel+1;
    ti = ti+1
##print "Total cost: ", t_cost
count_t = 0

for x in schedule:
    for y in x:
	if y==1:
	    count_t = count_t + 1
print " "
print "Total on generators: ", count_t
print "total cost of running: ", t_cost
print("--- %s seconds ---" % (time.time() - start_time))
wb.save('Output_Matrices_instance_' + str(instance)) 


        