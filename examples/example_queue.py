"""
Bank with multiple queues example

Covers:
- Resources: Resource
- Iterating processes

Scenario:
  A multi-counter bank with a random service time and customers arrival process. Based on the
  program bank10.py from TheBank tutorial of SimPy 2. (KGM)

By Aaron Janeiro Stone
"""

from simpy import *
import random

maxNumber = 30      # Max number of customers
maxTime = 400.0     # Rumtime limit
timeInBank = 20.0   # Mean time in bank
arrivalMean = 10.0  # Mean of arrival process
seed = 12345        # Seed for simulation


def Customer(env, name, counters):
    
    arrive = env.now  # log arrival time
    Qlength = [NoInSystem(counters[i]) for i in range(len(counters))]  # store current queue lengths
    print("%7.4f %s: Here I am. %s" % (env.now, name, Qlength))
    
    # Choose the shortest queue:
    for i in range(len(Qlength)):
        if Qlength[i] == 0 or Qlength[i] == min(Qlength):
            choice = i
            break
    
    # Request one of the counters:
    with counters[choice].request() as req:
        # Wait in queue until turn comes:
        yield req

        # Announce arrival:        
        wait = env.now - arrive
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        
        # Randomly select the service time from an exponential distribution:
        tib = random.expovariate(1.0 / timeInBank)
        yield env.timeout(tib)
        print('%7.4f %s: Finished' % (env.now, name))


def NoInSystem(R: Resource):
    """Total number of customers in the resource R"""
    return max([0, len(R.put_queue) + len(R.users)])


# Define the arrival process (number of customers and inter-arrival time):
def Source(env, number, interval, counters):
    for i in range(number):
        c = Customer(env, 'Customer%02d' % i, counters)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


# Setup and start the simulation
print('Bank with multiple queues')
random.seed(seed)
env = Environment()

counters = [Resource(env), Resource(env)]
env.process(Source(env, maxNumber, arrivalMean, counters))
env.run(until=maxTime)
