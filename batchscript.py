from  main import main
import numpy as np

# Simulation params
n_servers = 2
discipline = 'FIFO'
mean_service_rate = 1
max_customers = 1_000_000
max_runtime = 100_000
# seed = 69420

utilization = np.linspace(0.5,0.99,5)
servers = [1,2,4]
time = np.linspace(10000,200000,10)
for u in utilization:
    for n in servers:
        for t in time:
            u = round(u,3)
            mean_arrival_rate = u * n # ensures system load same for all n
            result ,expected,measured= main(n, discipline, mean_service_rate, mean_arrival_rate, max_customers, t)
            result =[ [result[0][i],result[1][i]] for i in range(len(result[0]))]
            np.savetxt('result xm{} m{} v{} n{} p{} t{}.csv'.format(expected['expected waiting time'],measured['Average waiting time'][0],measured['Average waiting time'][1],n,u,t), result, delimiter=",")
