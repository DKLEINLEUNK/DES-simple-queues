import simpy
import random
import numpy as np
# import pandas as pd


class QueueSimulation:
    
    '''
    Handles simulation of queueing system.
    '''
    
    def __init__(self, n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers, max_runtime, seed=None, B="M"):
        
        '''
        Initializes the simulation environment and parameters.
        '''

        if seed is not None: random.seed(seed)

        # Initialize simulation environment:
        self.env = simpy.Environment()

        # Initialize simulation parameters:
        self.n_servers = n_servers
        self.discipline = discipline
        self.mean_service_rate = mean_service_rate
        self.mean_arrival_rate = mean_arrival_rate
        self.max_customers = max_customers
        self.max_runtime = max_runtime
        
        # Initialize log:
        self.waiting_times = np.full(max_customers, np.NaN)
        self.queue_lengths = np.full(max_customers, np.NaN)

        # Initialize service time distribution:
        distributions = {
            "M": random.expovariate,
            "D": lambda x : x,
            "H": lambda x : 0.75 * random.expovariate(1.0) + 0.25 * random.expovariate(5.0) 
        }
        self.service_distribution = distributions[B]


    def run(self):
        
        '''
        Initializes server and starts arrivals.
        '''

        self.server = simpy.PriorityResource(self.env, capacity=self.n_servers)
        self.env.process(self.arrivals())
        self.env.run(until=self.max_runtime)

        self.waiting_times = self.waiting_times[~np.isnan(self.waiting_times)]
        self.queue_lengths = self.queue_lengths[~np.isnan(self.queue_lengths)]


    def arrivals(self):
        
        '''
        Handles customer arrivals.
        '''

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
        
        '''
        Handles customer service upon arrival. 
        Depends on server discipline.
        '''

        # Assess system state upon arrival:
        # np.append(self.queue_lengths, len(self.server.put_queue))  # NOTE: does order matter here?
        self.queue_lengths[id] = len(self.server.put_queue)
        # in_system = in_queue + len(self.server.users)

        arrival_time = self.env.now

        # Prepare service:
        t_inter_service = self.service_distribution(self.mean_service_rate)
        
        # Check for discipline:
        if self.discipline == 'FIFO': prio = 0  # all customers have equal priority
        elif self.discipline == 'SJF': prio = t_inter_service  # shorter jobs have higher priority

        with self.server.request(priority=prio) as request:
            
            # Wait in queue until turn comes:
            yield request
            
            # Arrival at server:
            # np.append(self.queue_lengths, len(self.server.put_queue))  # NOTE: does order matter here?
            self.waiting_times[id] = self.env.now - arrival_time
            
            # print("[%7.4fs] ID %s: Arrived (waited %6.3fs)" % (self.env.now, id, waiting_time))

            # Service:
            yield self.env.timeout(t_inter_service)

            # print("[%7.4fs] ID %s: Finished." % (self.env.now, id))


    def get_log(self):

        '''
        Returns `waiting_times` and `queue_lengths`.
        '''
        
        return self.waiting_times, self.queue_lengths
