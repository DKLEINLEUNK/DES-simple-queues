import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class QueueSimulation:
    
    '''Handles simulation of queueing system.'''
    
    def __init__(self, n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers, max_runtime, seed=None):
        
        '''Initializes the simulation environment and parameters.'''

        if seed is not None: random.seed(seed)

        self.env = simpy.Environment()

        self.n_servers = n_servers
        self.discipline = discipline
        self.mean_service_rate = mean_service_rate
        self.mean_arrival_rate = mean_arrival_rate
        self.max_customers = max_customers
        self.max_runtime = max_runtime

        self.log = pd.DataFrame(columns=['ID', 'Arrival time', 'Waiting time', 'Service time', 'Departure time', 'in_queue', 'in_system'])


    def run(self):
        
        '''Initializes server resources based on discipline.'''

        if self.discipline == 'FIFO':
            
            self.server = simpy.Resource(self.env, capacity=self.n_servers)
            self.env.process(self.arrivals())
            self.env.run(until=self.max_runtime)


    def arrivals(self):
        
        '''Handles customer arrivals.'''

        customer_id = 0
        
        while customer_id < self.max_customers:
            
            customer_id += 1

            # Serve new customer:
            new_customer = self.customer(customer_id)
            self.env.process(new_customer)
            
            # Wait for next customer (assuming exponential inter-arrival times):
            t_inter_arrival = random.expovariate(self.mean_arrival_rate)
            yield self.env.timeout(t_inter_arrival)


    def customer(self, id):
        
        '''Handles customer service upon arrival.'''

        # Assess system state on arrival:
        in_queue = len(self.server.put_queue)
        in_system = in_queue + len(self.server.users)

        arrival_time = self.env.now
        
        with self.server.request() as request:    
            
            # Wait in queue until turn comes:
            yield request
            
            # Arrival at server:
            waiting_time = self.env.now - arrival_time
            
            # print("[%7.4fs] ID %s: Arrived (waited %6.3fs)" % (self.env.now, id, waiting_time))

            # Service (exponential inter-service times):
            t_inter_service = random.expovariate(self.mean_service_rate)
            yield self.env.timeout(t_inter_service)

            # Log data on departure:
            customer_data = {
                'ID': id,
                'Arrival time': arrival_time,
                'Waiting time': waiting_time,
                'Service time': t_inter_service,
                'Departure time': self.env.now,
                'in_queue': in_queue,
                'in_system': in_system
            }

            self.log = self.log._append(customer_data, ignore_index=True)
            
            # print("[%7.4fs] ID %s: Finished." % (self.env.now, id))


    def analyze_results(self):
        
        # TODO Implement analysis and plotting of results
        
        pass
