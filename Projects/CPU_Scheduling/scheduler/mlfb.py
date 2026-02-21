from collections import deque
from utils.metrics import Metrics
from utils.mlfq_rich_table import MLFQRichTable


class MLFQScheduler:
    def __init__(self, config, api, logger):
        self.config = config
        self.api = api
        self.logger = logger
        self.metrics = Metrics()

        # Initialize queues with priority, quantum, and aging
        self.queues = [
            {'queue': deque(), 'quantum': quantum, 'priority': idx + 1}
            for idx, quantum in enumerate(config["TimeQuantums"])
        ]
        self.aging_threshold = config["AgingThreshold"]

        # Initialize CPU and I/O resources dynamically
        self.running_queue = [None] * config["cpus"]
        self.io_devices = [None] * config["ios"]

        self.terminated_jobs = []
        self.job_data = {}  # To track job-specific data (arrival time, total burst, etc.)
        self.visualizer = MLFQRichTable()  # Use the custom RichTable for MLFQ
        self.cpu_busy_time = 0  # Track total CPU busy time

    def run_simulation(self, session_id, start_clock):
        clock = start_clock
        self.metrics.total_time = 0  # Track total simulation time

        while True:
            self.metrics.total_time += 1  # Increment simulation time
            self.logger.info(f"Clock: {clock}")

            # Fetch new jobs
            new_jobs = self.api.get_jobs(session_id, clock)
            if new_jobs:
                for job in new_jobs:
                    job_id = job["job_id"]
                    burst = self.api.get_burst(session_id, job_id)
                    if burst:
                        job["burst_time"] = burst["duration"]
                        job["priority"] = 1  # Start at highest priority
                        self.job_data[job_id] = {
                            "arrival_time": clock,
                            "total_burst_time": burst["duration"],
                            "completion_time": None,
                            "waiting_time": 0,
                        }
                        self.queues[0]["queue"].append(job)
                        self.logger.info(f"Job {job_id} added to Queue 1 with burst time {job['burst_time']}")

            # Assign jobs from queues to CPUs
            for cpu_index in range(len(self.running_queue)):
                if not self.running_queue[cpu_index]:
                    for queue_data in self.queues:
                        if queue_data["queue"]:
                            job = queue_data["queue"].popleft()
                            self.running_queue[cpu_index] = {
                                "job": job,
                                "quantum_remaining": queue_data["quantum"],
                            }
                            self.logger.info(f"Job {job['job_id']} assigned to CPU {cpu_index} from Queue {queue_data['priority']}")
                            break

            # Process running jobs
            for cpu_index, running_job_info in enumerate(self.running_queue):
                if running_job_info:
                    job = running_job_info["job"]
                    running_job_info["quantum_remaining"] -= 1
                    job["burst_time"] -= 1
                    self.cpu_busy_time += 1

                    self.logger.info(
                        f"CPU {cpu_index} processing Job {job['job_id']} - Remaining Burst Time: {job['burst_time']}, Quantum Remaining: {running_job_info['quantum_remaining']}"
                    )

                    # Handle job completion
                    if job["burst_time"] == 0:
                        self.logger.info(f"Job {job['job_id']} completed at clock {clock}")
                        bursts_left = self.api.bursts_left(session_id, job["job_id"])

                        if bursts_left > 1:
                            next_burst = self.api.get_burst(session_id, job["job_id"])
                            if next_burst:
                                job["burst_time"] = next_burst["duration"]
                                job["priority"] = 1  # Reset to highest priority
                                self.queues[0]["queue"].append(job)
                                self.logger.info(f"Job {job['job_id']} re-added to Queue 1")
                        else:
                            self.terminated_jobs.append(job)
                            turnaround_time = clock - self.job_data[job["job_id"]]["arrival_time"]
                            waiting_time = turnaround_time - self.job_data[job["job_id"]]["total_burst_time"]
                            self.job_data[job["job_id"]]["completion_time"] = clock
                            self.metrics.add_job_stats(turnaround_time, waiting_time)
                            self.logger.info(f"Job {job['job_id']} has terminated")
                        self.running_queue[cpu_index] = None
                    # Handle quantum expiration
                    elif running_job_info["quantum_remaining"] == 0:
                        next_priority = min(job["priority"] + 1, len(self.queues))
                        job["priority"] = next_priority
                        self.queues[next_priority - 1]["queue"].append(job)
                        self.logger.info(f"Job {job['job_id']} demoted to Queue {next_priority}")
                        self.running_queue[cpu_index] = None

            # Update visualization
            self.visualizer.show_tables(
                [
                    [
                        f"Job {job['job_id']} (P{queue['priority']})"
                        for job in queue["queue"]
                    ]
                    for queue in self.queues
                ],
                [
                    f"CPU {i} [Job: {j['job']['job_id']} (P{j['job']['priority']}), Remaining: {j['job']['burst_time']}]"
                    if j else "Idle" for i, j in enumerate(self.running_queue)
                ],
                [f"Job {job['job_id']}" for job in self.terminated_jobs],
            )

            # Exit condition
            if not any(queue["queue"] for queue in self.queues) and not any(self.running_queue) and not any(self.io_devices) and self.api.jobs_left(session_id) == len(self.terminated_jobs):
                self.logger.info("All jobs completed!")
                break

            clock += 1

        # Log metrics
        avg_turnaround, avg_waiting, cpu_utilization = self.metrics.calculate()
        self.logger.info(f"Average Turnaround Time: {avg_turnaround}")
        self.logger.info(f"Average Waiting Time: {avg_waiting}")
        # Correct CPU utilization calculation
        cpu_utilization = (self.cpu_busy_time / (self.metrics.total_time * len(self.running_queue))) * 100 if self.metrics.total_time > 0 else 0
        self.logger.info(f"CPU Utilization: {cpu_utilization:.2f}%")

        # Log turnaround time and waiting time for each job
        self.logger.info("Job Turnaround and Waiting Times:")
        for job_id, data in self.job_data.items():
            turnaround_time = data["completion_time"] - data["arrival_time"]
            waiting_time = turnaround_time - data["total_burst_time"]
            self.logger.info(f"Job {job_id} - Turnaround Time: {turnaround_time}, Waiting Time: {waiting_time}")
