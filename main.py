from Queue import *
from Metrics import *
import sys 

# For testing purposes:
import time

def main():

    # Simulation params
    n_servers = 2
    discipline = 'FIFO'
    mean_service_rate = 3.5
    mean_arrival_rate = 3 * n_servers # ensures system load same for all n
    max_customers = 100_000
    max_runtime = 10_000
    seed = 69420

    print('Running queueing system simulation...')
    simulation = QueueSimulation(n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers, max_runtime, seed)
    simulation.run()

    print('Simulation finished!')
    print('')
    Metrics = QueueMetrics(simulation)
    expected_metrics = Metrics.get_expected_metrics()
    measured_metrics = Metrics.get_measured_metrics()

    print("EXPECTED")
    for key, value in expected_metrics.items():
        print(f"{key} = {value:.3f}")

    print("\nMEASURED")
    for key, value in measured_metrics.items():
        print(f"{key} = {value[0]:.3f}, Variance: {value[1]}")

    return simulation.get_log()


if __name__ == '__main__':    
    waiting_lists, queue_lengths = main()

    print(f"\nn_wait: {waiting_lists.size}")
    print(f"n_queue: {queue_lengths.size}")  # idk why these values are different...
