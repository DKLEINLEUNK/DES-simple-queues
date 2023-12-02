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
        self.waiting_times = np.array([])
        self.queue_lengths = np.array([])
        self.t = np.full(max_customers, np.NaN)
        self.N_t = np.full(max_customers, np.NaN)

        # Initialize service time distribution:
        distributions = {
            "M": random.expovariate,
            "D": lambda x : 1/x,
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

        # Remove NaNs from logged data:
        self.t = self.t[~np.isnan(self.t)]
        self.N_t = self.N_t[~np.isnan(self.N_t)]

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
        self.queue_lengths = np.append(self.queue_lengths, len(self.server.put_queue))  # NOTE: does order matter here?
        t, N_t = self.get_N_t()

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
            self.waiting_times = np.append(self.waiting_times, self.env.now - arrival_time)  # NOTE: does order matter here?
            
            # print("[%7.4fs] ID %s: Arrived (waited %6.3fs)" % (self.env.now, id, waiting_time))

            # Service:
            yield self.env.timeout(t_inter_service)

            # print("[%7.4fs] ID %s: Finished." % (self.env.now, id))


    def get_N_t(self):
        '''
        Returns the number of customers in the system at time t.
        '''
        N = len(self.server.users) + len(self.server.put_queue)
        t = self.env.now
        return t, N

    def get_A_t(self):
        '''
        Returns arrivals and time t.
        '''
        t = self.env.now
        return t, self.mean_arrival_rate

    def get_log(self):

        '''
        Returns `waiting_times` and `queue_lengths`.
        '''
        
        return self.waiting_times, self.queue_lengths
