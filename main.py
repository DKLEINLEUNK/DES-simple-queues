from Queue import *
from Metrics import *
from helpers import error_message
import argparse

# For testing purposes:
import time

def main(queue_system, n, arrival_rate, service_rate, max_runtime, max_customers, discipline, save, save_raw):
    # Simulation params
    n_servers = int(queue_system[2])
    B = queue_system[1]
    avg_waiting_times, avg_queue_lengths = np.zeros(n), np.zeros(n)

    # Running n simulations
    for i in range(n):
        print(f'Running queueing system simulation {i+1}/{n}...       ', end="\r")

        simulation = QueueSimulation(n_servers, discipline, service_rate, arrival_rate, max_customers, max_runtime, B=B, seed=i)
        simulation.run()

        # save average results
        waiting_lists, queue_lengths = simulation.get_log()
        avg_waiting_times[i] = np.mean(waiting_lists)
        avg_queue_lengths[i] = np.mean(queue_lengths)

        Metrics = QueueMetrics(simulation)
        if save_raw:
            Metrics.to_csv(queue_system, seed=i)
        
    
    print('\nAll simulations finished!')
    print('')

    # save average metrics to csv
    if save:
        data = np.vstack((avg_waiting_times, avg_queue_lengths)).T
        title = f"averages_{queue_system}_n{n}_rho{Metrics.rho}_max_runtime{simulation.max_runtime}_{simulation.discipline}.csv"
        np.savetxt("./data/simulation_averages/"+ title, data, delimiter=',', header="avg_waiting_times, avg_queue_lengths")
        print(f"Output saved to {title}")
    

    print("EXPECTED")
    expected_metrics = Metrics.get_expected_metrics()
    for key, value in expected_metrics.items():
        print(f"{key} = {value:.3f}")

    print("\nMEASURED AVERAGE(S)")
    for wait_time, length in zip(avg_waiting_times, avg_queue_lengths):
        print(f"Average queue length: {length:.3f}, Average wait time: {wait_time:.3f} ")

    waiting_lists, queue_lengths =  simulation.get_log()
    print("*****SUPER MEANS *****")
    print("Waiting time:", np.mean(avg_waiting_times))
    print("Avg queue lengths", np.mean(avg_queue_lengths))

    print(f"\nn_wait: {waiting_lists.size}")
    print(f"n_queue: {queue_lengths.size}")  


if __name__ == '__main__':
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Simulate queueing systems and measure performance")

    # adding arguments
    parser.add_argument("queue_system", help="Queueing system to use in kendall notation, f.e. MM1")
    parser.add_argument("run_time", help="max run_time used per simulation", default=10**4, type=int)
    parser.add_argument("-c", "--customers", help="max customers arriving in one simulation", default=10**5, type=int)
    parser.add_argument("-l", "--arrival_rate", help="mean arrival rate (lambda)", default=0.9, type=float)
    parser.add_argument("-m", "--service_rate", help="mean service rate (mu)", default=1, type=float)
    parser.add_argument("-d", "--discipline", help="how to select from queue (FIFO or SJF)", default="FIFO")
    parser.add_argument("-n", help="number of simulations", default=1, type=int)
    parser.add_argument("--save", action="store_true", help="store average results in csv")
    parser.add_argument("--save_raw", action="store_true", help="store all data in csv for each simulation")

    # read arguments from command line
    args = parser.parse_args()

    # print error if arguments invalid, else run main with provided arguments
    error = error_message(args)
    if error:
        print(error)
    else:
        main(
            args.queue_system, args.n, args.arrival_rate, args.service_rate, 
            args.run_time, args.customers, args.discipline, args.save, args.save_raw
            )    