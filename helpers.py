import math

def error_message(args):
    """
    Checks command line arguments for invalid input.
    Returns error message if input invalid, else None.
    """
    if len(args.queue_system) != 3:
        return "Incorrect queue system format. Correct example: MM1"
    elif args.queue_system[0] != "M":
        return "Ärrival rate may only be Markovian"
    elif args.queue_system[1] not in ["M", "D", "H"]:
        return "Service time distribution must be M, D or H"
    elif args.arrival_rate / (args.service_rate * int(args.queue_system[-1])) >= 1:
        return "Service utilization rho must be smaller than one"
    elif args.discipline not in ["FIFO", "SJF"]:
        return "Queue discipline must be FIFO or SJF (shortest jobs first)"
    return None


def calc_p0(rho, c):
    """
    Returns probability customer visits an empty system.
    """
    
    if c == 1:
        return 1 - rho
    else:
        s = 0
        for k in range(c):
            # summation
            s += (c * rho)**k / math.factorial(k)

        # add last component
        s += (c * rho)**c / (math.factorial(c) * (1 - rho))
        p_0 = s**(-1)
        return p_0


def calc_delay_prob(p_0, rho, c):
    """
    Returns probability customer will have to wait for service.
    """
    if c == 1:
        return rho
    else:
        p_c = p_0 * ((c * rho)**c / math.factorial(c))
        p_d = p_c / (1 - rho)
        return p_d


def calc_exp_length(delay_prob, rho):
    """
    Queue length using little's law - excludes service
    """ 
    return delay_prob * (rho / (1 - rho))


def calc_exp_wait(rho, c, service_rate):
    """
    Queue wait time using little's law - excludes service
    """
    p0 = calc_p0(rho, c)
    delay_prob = calc_delay_prob(p0, rho, c)
    return delay_prob / (c * service_rate * (1 - rho))