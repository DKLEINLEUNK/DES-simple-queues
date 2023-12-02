'''
This file contains relevant functions for time series analysis.
'''

# Imports:
from Queue import *
import matplotlib.pyplot as plt

# Data generation:
m_m_1 = QueueSimulation(
    n_servers= 1,
    discipline= 'FIFO',
    mean_service_rate= 3.5,
    mean_arrival_rate= 3,
    max_customers= 500_000,
    max_runtime= 150_000,
    seed= None,
    B= 'M'
)
m_m_1.run()

t = m_m_1.t

N_t = m_m_1.N_t
cumsum = np.cumsum(N_t)
i = np.arange(1, len(N_t) + 1)
N_t_mean = cumsum / i  # cumulative mean

# Data visualization:
plt.plot(t, N_t_mean)
plt.xlabel('Time')
plt.ylabel('Mean number of customers in system')
plt.title(f'M/M/1 Queue, $\\lambda = {m_m_1.mean_arrival_rate}$, $\\mu = {m_m_1.mean_service_rate}$')
plt.show()
