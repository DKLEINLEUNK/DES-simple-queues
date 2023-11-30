# import simpy
# import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

class QueueMetrics:
    
    '''Handles metric calculation of queueing parameters.'''
    
    def __init__(self, n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers):
        
        '''Initializes the simulation parameters and metric calculations'''

        self.n_servers = n_servers
        self.discipline = discipline
        self.mean_service_rate = mean_service_rate
        self.mean_arrival_rate = mean_arrival_rate
        self.max_customers = max_customers
    
        self.server_ut = self.mean_arrival_rate/self.mean_service_rate

        # utilization must be less than one for an exponentially distributed system
        assert self.server_ut < 1


    def calc_p0(self):
        rho = self.server_ut
        c = self.n_servers

        # probability customer visits an empty system
        if c == 1:
            return 1-rho
        else:
            s = 0
            for k in range(c):
                # summation
                s+=(c*rho)**k/math.factorial(k)
            # add last component
            s +=(c*rho)**c/(math.factorial(c)*(1-rho))
            p_0 = s**(-1)
            return p_0

    def calc_delay_prob(self,p_0):
        c = self.n_servers
        rho = self.server_ut

        # probability customer will have to wait for service
        if c == 1:
            return rho
        else:
            p_c = p_0*((c*rho)**c/math.factorial(c))
            p_d = p_c/(1-rho)
            return p_d

    def calc_exp_length(self,delay_prob):
        # Queue length using little's law - excludes service
        return delay_prob*(self.server_ut/(1-self.server_ut))
    
    def calc_exp_wait(self,delay_prob):
        # Queue wait time using little's law - excludes service
        return delay_prob/(self.n_servers*self.mean_service_rate*(1-self.server_ut))
    
    def run(self):

        p_0 = self.calc_p0()
        delay_prob = self.calc_delay_prob(p_0)
        queue_length = self.calc_exp_length(delay_prob)
        queue_wait = self.calc_exp_wait(delay_prob)

        return p_0,delay_prob,queue_length,queue_wait

