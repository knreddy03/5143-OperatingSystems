import sys
import json
import random
from utils.api_utils import APIUtils
from utils.logger import Logger
from scheduler.fcfs import FCFS
from scheduler.rr import RoundRobin
from scheduler.mlfb import MLFQScheduler
from scheduler.priority import PriorityScheduling


def parse_arguments(argv):
    """
    Parse command-line arguments and return them as a dictionary.
    """
    args = {}
    for arg in argv[1:]:
        if "=" in arg:
            key, value = arg.split("=")
            args[key] = value
    return args

def load_config(config_path):
    """
    Load the configuration JSON file.
    """
    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)

def main():
    # Parse command-line arguments
    args = parse_arguments(sys.argv)

    # Ensure required arguments are provided
    required_args = ["sched", "cpus", "ios", "config"]
    for arg in required_args:
        if arg not in args:
            print(f"Error: Missing required argument '{arg}'")
            print("Usage: python3 main.py sched=FCFS cpus=2 ios=2 config=config/myConfig.json [seed=12345]")
            sys.exit(1)

    # Load the configuration from the JSON file
    config = load_config(args["config"])
    config["cpus"] = int(args["cpus"])  # Number of CPUs
    config["ios"] = int(args["ios"])    # Number of IO devices

    # Extract optional seed from arguments
    seed = int(args["seed"]) if "seed" in args else None
    if seed:
        config["seed"] = seed  # Set the seed in the config for reproducibility

    # Set random seed for reproducibility
    if seed:
        random.seed(seed)

    # Initialize the APIUtils with the configuration
    api = APIUtils(config)

    # Initialize the session with the API
    try:
        session_data = api.init_session(seed=seed)
        session_id = session_data["session_id"]
        start_clock = session_data["start_clock"]
        time_slice = session_data["time_slice"]
        print(f"Initialized session {session_id} with start clock {start_clock}.")
    except RuntimeError as e:
        print(f"Error initializing session: {str(e)}")
        sys.exit(1)

    # Dynamically select the scheduler
    schedulers = {
        "FCFS": FCFS,
        "RoundRobin": RoundRobin,
        "MLFQScheduler": MLFQScheduler,
        "PriorityScheduling": PriorityScheduling
    }

    if args["sched"] not in schedulers:
        print(f"Error: Unsupported scheduler '{args['sched']}'. Supported schedulers: {', '.join(schedulers.keys())}")
        sys.exit(1)

    # Initialize the Scheduler
    scheduler_class = schedulers[args["sched"]]
    scheduler = scheduler_class(
        config=config,
        api=api,
        logger=Logger(),
    )
    
    # Run the simulation
    if args["sched"] == "FCFS":
        scheduler.run_simulation(session_id, start_clock)
    elif args["sched"] == "RoundRobin":
        scheduler.run_simulation(session_id, start_clock, time_slice)
    elif args["sched"] == "PriorityScheduling":
        scheduler.run_simulation(session_id, start_clock)
    elif args["sched"] == "MLFQScheduler":
        scheduler.run_simulation(session_id, start_clock)

if __name__ == "__main__":
    main()
