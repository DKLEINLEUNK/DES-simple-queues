import simpy
import random
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

        self.data = []  # for collecting statistics


    def run(self):
        
        '''Initializes server resources based on discipline.'''
        
        if self.discipline == 'FIFO':
            
            self.server = simpy.Resource(self.env, capacity=self.n_servers)
            self.env.process(self.arrivals())
            self.env.run(until=self.max_runtime)


    def arrivals(self):
        
        customer_id = 0
        
        while customer_id < self.max_customers:
            
            customer_id += 1

            # Create new customer:
            new_customer = self.customer(customer_id)
            self.env.process(new_customer)
            
            # Wait for next customer (assuming exponential inter-arrival times):
            t_inter_arrival = random.expovariate(1 / self.mean_arrival_rate)
            yield self.env.timeout(t_inter_arrival)


    def customer(self, id):

        arrival_time = self.env.now
        
        with self.server.request() as request:    
            
            # Wait in queue until turn comes:
            yield request
            
            # Announce arrival at server:
            waiting_time = self.env.now - arrival_time
            print("[%7.4fs] ID %s: Arrived (waited %6.3fs)" % (self.env.now, id, waiting_time))

            # Assumes exponential inter-service times
            t_inter_service = random.expovariate(1 / self.mean_service_rate)
            yield self.env.timeout(t_inter_service)
            print("[%7.4fs] ID %s: Finished." % (self.env.now, id))

            # self.data.append((self.env.now, service_start, service_end))  # TODO Implement data collection
        

    def analyze_results(self):
        
        # TODO Implement analysis and plotting of results
        
        pass
