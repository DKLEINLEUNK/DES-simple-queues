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