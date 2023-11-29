from Queue import *


def main():

    print('Running queueing system simulation...')

    simulation = QueueSimulation(
        n_servers = 2,
        discipline = 'FIFO',
        mean_service_rate = 1,
        mean_arrival_rate = 1, 
        max_customers = 50,
        max_runtime = 100,
        seed = 69420
    )
    
    simulation.run()
    
    print('Simulation finished! \n\nLog:')
    print(simulation.log)

    simulation.analyze_results()  # TODO Implement this method


if __name__ == '__main__':
    main()
