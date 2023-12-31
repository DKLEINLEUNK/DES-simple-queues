# import simpy
# import random
import numpy as np
import pandas as pd
import math

class QueueMetrics:
    
    '''
    Handles analytic metric calculation of queueing parameters.
    '''
    
    def __init__(self, queue_object):
        '''
        Description
        -----------
        Initializes the simulation parameters and metric calculations

        Parameters
        ----------
        queue_object : `class` QueueSimulation
        '''

        self.simulation = queue_object
        self.c = queue_object.n_servers
        self.service_rate = queue_object.mean_service_rate
        self.arrival_rate = queue_object.mean_arrival_rate
    
        self.rho = self.arrival_rate/(self.c * self.service_rate)

        # utilization must be less than one for an exponentially distributed system
        assert self.rho < 1


    def calc_p0(self):
        '''
        Description
        -----------
        Calculates the probability that the system is empty.
        I.e., customer visits an empty system.
        '''

        if self.c == 1:
            return 1 - self.rho
        else:
            s = 0
            for k in range(self.c):
                # summation
                s += (self.c * self.rho)**k / math.factorial(k)
            # add last component
            s += (self.c * self.rho)**self.c / (math.factorial(self.c) * (1 - self.rho))
            p_0 = s**(-1)
            return p_0


    def calc_delay_prob(self ,p_0):
        '''
        Description
        -----------
        Calculates the probability that a customer will have to wait for service.

        Parameters
        ----------
        p_0 : `float` probability that the system is empty
        '''

        # probability customer will have to wait for service
        if self.c == 1:
            return self.rho
        else:
            p_c = p_0 * ((self.c * self.rho)**self.c / math.factorial(self.c))
            p_d = p_c / (1 - self.rho)
            return p_d


    def calc_exp_length(self, delay_prob):
        '''
        Description
        -----------
        Calculates the expected queue length.

        Parameters
        ----------
        delay_prob : `float` probability that a customer will have to wait for service
        '''
        # Queue length using little's law - excludes service
        return delay_prob * (self.rho / (1 - self.rho))


    def calc_exp_wait(self, delay_prob):
        '''
        Description
        -----------
        Calculates the expected waiting time.

        Parameters
        ----------
        delay_prob : `float` probability that a customer will have to wait for service
        '''
        # Queue wait time using little's law - excludes service
        return delay_prob / (self.c * self.service_rate * (1 - self.rho))


    def get_expected_metrics(self):
        """
        Description
        -----------
        Returns a dict with expected performance measures.
        """

        p_0 = self.calc_p0()
        delay_prob = self.calc_delay_prob(p_0)

        metrics = {
            'p_0': p_0,
            'delay probability': delay_prob,
            'expected queue length': self.calc_exp_length(delay_prob),
            'expected waiting time': self.calc_exp_wait(delay_prob)
        }

        return metrics


    def get_measured_metrics(self):
        """
        Description
        -----------
        Returns dict with value: (mean performance metric, variance)
        """
        waiting_times = self.simulation.waiting_times
        queue_lengths = self.simulation.queue_lengths
        metrics = {
            "Average waiting time": (np.mean(waiting_times), np.var(waiting_times)),
            "Average queue length": (np.mean(queue_lengths), np.var(queue_lengths)),
        }

        return metrics 

    def to_csv(self, queue_type, seed):
        """
        Saves raw data of simulation to csv. 
        """
        waiting_times, queue_lengths = self.simulation.get_log()
        queue_lengths = queue_lengths[:waiting_times.size] # splice to make equal length
        
        data = np.vstack((waiting_times, queue_lengths)).T
        title = f"./data/raw_data/{queue_type}_seed{seed}_rho{self.rho}_max_runtime{self.simulation.max_runtime}_lambda_{self.simulation.mean_arrival_rate}.csv"
        np.savetxt(title, data, delimiter=',', header="waiting_times,queue_lengths")
        return