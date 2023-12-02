import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from Queue import *
from Metrics import *

'''
Queuing theory tells us that for FIFO scheduling 
the average waiting times are shorter for an M/M/n 
queue and a system load ρ and processor capacity µ 
than for a single M/M/1 queue with the same load 
characteristics (and thus an n-fold lower arrival rate).

Of course, ρ must be less than one, but the experiment
only becomes interesting when ρ is not much less than one.

The following code snippet shows that the average waiting
time for an M/M/1 queue is much longer than for an M/M/n
queue with the same load characteristics, using FIFO 
discipline for n=1, n=2, and n=4.
'''

# Run M/M/n simulations for n=1,2,4:
def avg_waiting_times(n_servers, max_iterations):
    
    '''
    Runs `max_iterations` simulations of M/M/`n_servers` system.
    Returns the average waiting time for each simulation.
    '''

    result = np.zeros(max_iterations)

    arrival_rate = (3 * n_servers)  # ensures system load same for all n
    server_capacity = 3.2
    system_load = arrival_rate / (server_capacity * n_servers)
    max_customers = 1_000

    print(f'\nUsing parameters rho = {round(system_load, 3)} and N = {max_customers}.')
    print(f'Starting {max_iterations} iterations for M/M/{n_servers}...')
    
    for i in np.arange(max_iterations):

        MMn = QueueSimulation(
            n_servers= n_servers,
            discipline= 'FIFO',
            mean_service_rate= server_capacity,
            mean_arrival_rate= arrival_rate,
            max_customers= max_customers,
            max_runtime= 10_000,
            seed= None,
            B= 'M'
        )

        MMn.run()

        #------------------------
        # Compare with theory:
        #------------------------
        Metrics = QueueMetrics(MMn)
        expected_metrics = Metrics.get_expected_metrics()
        measured_metrics = Metrics.get_measured_metrics()

        print("EXPECTED")
        for key, value in expected_metrics.items():
            print(f"{key} = {value:.3f}")

        print("\nMEASURED")
        for key, value in measured_metrics.items():
            print(f"{key} = {value[0]:.3f}, Variance: {value[1]}")

        # Store result:
        result[i] = MMn.waiting_times.mean()

    print(f'Completed {max_iterations} iterations for n={n_servers}!')

    return result

# Make sure that your result has a high 
# and known statistical significance. 
# How does the number of measurements
# required to attain this depend on ρ?

# Run simulations:
MM1 = avg_waiting_times(n_servers=1, max_iterations=1)
MM2 = avg_waiting_times(n_servers=2, max_iterations=1)
MM4 = avg_waiting_times(n_servers=4, max_iterations=1)

breakpoint()

print('')
print('Mean average waiting times per system:')
print("MM1:", MM1.mean())
print("MM2:", MM2.mean())
print("MM4:", MM4.mean())
print('')



#------------------------
# Statistical analysis:
#------------------------

print('')
# Check assumptions of ANOVA:
for i, group in enumerate([MM1, MM2, MM4], 1):
    stat, p = stats.shapiro(group)
    print(f'Group {i} - Shapiro-Wilk Test: Statistics={stat:.3f}, p={p:.3f}') # p > 0.05, normal distribution

stat, p = stats.levene(MM1, MM2, MM4)
print(f'Levene’s Test: Statistics={stat:.3f}, p={p:.3f}') # p > 0.05, variances are equal

# Q-Q plots:
plt.figure(figsize=(12, 4))
for i, group in enumerate([MM1, MM2, MM4], 1):
    plt.subplot(1, 3, i)
    stats.probplot(group, dist="norm", plot=plt)
    plt.title(f'Group {i}')
plt.tight_layout()
plt.show() # normal distribution if points lie on the line

# Assumptions are not met, so we use Kruskal-Wallis test:
print('')
print('Assumptions not met, Kruskal-Wallis Test:')
stat, p = stats.kruskal(MM1, MM2, MM4)
print(f'Kruskal-Wallis Test: Statistic={stat:.3f}, p={p:.3f}') # p < 0.05, significant differences found between the groups


#------------------------
# Post-hoc testing:
#------------------------

print('')
stat, p = stats.mannwhitneyu(MM1, MM2)
print(f'Mann-Whitney U Test, MM1 & MM2: U={stat:.3f}, p={p:.3f}') # p < 0.05, significant differences found between the groups
stat, p = stats.mannwhitneyu(MM1, MM4)
print(f'MM1 & MM4: U={stat:.3f}, p={p:.3f}') # p < 0.05, significant differences found between the groups
stat, p = stats.mannwhitneyu(MM2, MM4)
print(f'MM2 & MM4: U={stat:.3f}, p={p:.3f}') # p < 0.05, significant differences found between the groups
print('')


#------------------------
# Plot results:
#------------------------

# Plot average waiting times:
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.hist(MM1, bins=25)
plt.xlim(0, 10)
plt.title('MM1')
plt.xlabel('Average waiting time')
plt.ylabel('Frequency')
plt.subplot(1, 3, 2)
plt.hist(MM2, bins=25)
plt.xlim(0, 10)
plt.title('MM2')
plt.xlabel('Average waiting time')
plt.ylabel('Frequency')
plt.subplot(1, 3, 3)
plt.hist(MM4, bins=25)
plt.xlim(0, 10)
plt.title('MM4')
plt.xlabel('Average waiting time')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
