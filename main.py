from Queue import *
from Metrics import *

def main():

    # Simulation params
    n_servers = 2
    discipline = 'FIFO'
    mean_service_rate = 0.9
    mean_arrival_rate = 0.72
    max_customers = 50
    max_runtime = 100
    seed = 69420

    # Queue metrics - using markov chains to determine probability of state and little's law
    calc = QueueMetrics(n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers)
    metrics = calc.run()
    print('p_0',metrics[0])
    print('delay_prob',metrics[1])
    print('avg_queue_length',metrics[2])
    print('avg_queue_wait',metrics[3])

    print('Running queueing system simulation...')
    simulation = QueueSimulation(n_servers, discipline, mean_service_rate, mean_arrival_rate, max_customers, max_runtime, seed)
    simulation.run()
    
    print('Simulation finished! \n\nLog:')
    print(simulation.log)

    simulation.analyze_results()  # TODO Implement this method


if __name__ == '__main__':
    main()
