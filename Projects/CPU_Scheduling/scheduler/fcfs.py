from utils.metrics import Metrics
from utils.rich_table import RichTable


class FCFS:
    def __init__(self, config, api, logger):
        self.config = config
        self.api = api
        self.logger = logger
        self.ready_queue = []  # For CPU-bound jobs
        self.waiting_queue = []  # For I/O-bound jobs
        self.running_queue = [None] * config["cpus"]  # Tracks jobs currently running on CPUs
        self.io_devices = [None] * config["ios"]  # Tracks jobs currently running on I/O devices
        self.terminated_jobs = []  # Stores jobs that have completed all bursts
        self.job_data = {}  # Track job arrival, burst times, and completion times
        self.metrics = Metrics()  # Initialize metrics
        self.visualizer = RichTable()  # Initialize RichTable for visualization
        self.cpu_busy_time = 0  # Track total CPU busy time

    def run_simulation(self, session_id, start_clock):
        clock = start_clock
        self.metrics.total_time = 0  # Track total simulation time

        while True:
            self.metrics.total_time += 1  # Increment total time for metrics calculation
            self.logger.info(f"Clock: {clock}")

            # Fetch new jobs and determine their initial placement
            new_jobs = self.api.get_jobs(session_id, clock)
            if new_jobs:
                for job in new_jobs:
                    job_id = job["job_id"]
                    burst = self.api.get_burst(session_id, job_id)
                    if burst:
                        job["burst_time"] = burst["duration"]
                        job["burst_type"] = burst["burst_type"]
                        self.job_data[job_id] = {
                            "arrival_time": clock,
                            "total_burst_time": burst["duration"],
                            "completion_time": None,
                        }
                        if burst["burst_type"] == "CPU":
                            self.ready_queue.append(job)
                            self.logger.info(f"Job {job_id} added to READY queue with burst time {job['burst_time']}")
                        elif burst["burst_type"] == "IO":
                            self.waiting_queue.append(job)
                            self.logger.info(f"Job {job_id} added to WAITING queue with burst time {job['burst_time']}")

            # Assign jobs from ready queue to CPUs
            for cpu_index in range(len(self.running_queue)):
                if not self.running_queue[cpu_index] and self.ready_queue:
                    job = self.ready_queue.pop(0)
                    self.running_queue[cpu_index] = {"cpu_id": cpu_index, "job": job, "remaining_time": job["burst_time"]}
                    self.logger.info(f"Job {job['job_id']} assigned to CPU {cpu_index}")

            # Assign jobs from waiting queue to I/O devices
            for io_index in range(len(self.io_devices)):
                if not self.io_devices[io_index] and self.waiting_queue:
                    job = self.waiting_queue.pop(0)
                    self.io_devices[io_index] = {"io_id": io_index, "job": job, "remaining_time": job["burst_time"]}
                    self.logger.info(f"Job {job['job_id']} assigned to I/O Device {io_index}")

            # Process jobs on CPUs
            for cpu_index, cpu_info in enumerate(self.running_queue):
                if cpu_info and cpu_info["job"]:
                    self.cpu_busy_time += 1  # Increment CPU busy time
                    cpu_info["remaining_time"] -= 1
                    self.logger.info(f"CPU {cpu_info['cpu_id']} processing Job {cpu_info['job']['job_id']} - Remaining Burst Time: {cpu_info['remaining_time']}")

                    # If burst is completed
                    if cpu_info["remaining_time"] == 0:
                        job = cpu_info["job"]
                        self.logger.info(f"Job {job['job_id']} completed CPU burst at clock {clock}")
                        bursts_left = self.api.bursts_left(session_id, job["job_id"])

                        if bursts_left > 1:
                            next_burst = self.api.get_burst(session_id, job["job_id"])
                            if next_burst:
                                job["burst_time"] = next_burst["duration"]
                                job["burst_type"] = next_burst["burst_type"]
                                if next_burst["burst_type"] == "CPU":
                                    self.ready_queue.append(job)
                                    self.logger.info(f"Job {job['job_id']} added back to READY queue with burst time {job['burst_time']}")
                                elif next_burst["burst_type"] == "IO":
                                    self.waiting_queue.append(job)
                                    self.logger.info(f"Job {job['job_id']} added to WAITING queue with burst time {job['burst_time']}")
                        else:
                            self.terminated_jobs.append(job)
                            self.logger.info(f"Job {job['job_id']} has completed all bursts and is now TERMINATED")

                            # Calculate turnaround and waiting times
                            turnaround_time = clock - self.job_data[job["job_id"]]["arrival_time"]
                            waiting_time = turnaround_time - self.job_data[job["job_id"]]["total_burst_time"]
                            self.job_data[job["job_id"]]["completion_time"] = clock
                            self.metrics.add_job_stats(turnaround_time, waiting_time)

                        # Free the CPU slot
                        self.running_queue[cpu_index] = None

            # Process jobs on I/O devices
            for io_index, io_info in enumerate(self.io_devices):
                if io_info and io_info["job"]:
                    io_info["remaining_time"] -= 1
                    self.logger.info(f"I/O Device {io_info['io_id']} processing Job {io_info['job']['job_id']} - Remaining Burst Time: {io_info['remaining_time']}")

                    # If I/O burst is completed
                    if io_info["remaining_time"] == 0:
                        job = io_info["job"]
                        self.logger.info(f"Job {job['job_id']} completed I/O burst at clock {clock}")
                        bursts_left = self.api.bursts_left(session_id, job["job_id"])

                        if bursts_left > 1:
                            next_burst = self.api.get_burst(session_id, job["job_id"])
                            if next_burst:
                                job["burst_time"] = next_burst["duration"]
                                job["burst_type"] = next_burst["burst_type"]
                                if next_burst["burst_type"] == "CPU":
                                    self.ready_queue.append(job)
                                    self.logger.info(f"Job {job['job_id']} added back to READY queue with burst time {job['burst_time']}")
                                elif next_burst["burst_type"] == "IO":
                                    self.waiting_queue.append(job)
                                    self.logger.info(f"Job {job['job_id']} added back to WAITING queue with burst time {job['burst_time']}")
                        else:
                            self.terminated_jobs.append(job)
                            self.logger.info(f"Job {job['job_id']} has completed all bursts and is now TERMINATED")

                            # Calculate turnaround and waiting times
                            turnaround_time = clock - self.job_data[job["job_id"]]["arrival_time"]
                            waiting_time = turnaround_time - self.job_data[job["job_id"]]["total_burst_time"]
                            self.job_data[job["job_id"]]["completion_time"] = clock
                            self.metrics.add_job_stats(turnaround_time, waiting_time)

                        # Free the I/O device slot
                        self.io_devices[io_index] = None

            # Update visualization
            self.visualizer.show_tables(
                self.ready_queue,
                self.waiting_queue,
                self.running_queue,
                self.io_devices,
                self.terminated_jobs,
            )

            # Exit condition: All queues and resources are empty
            if not any(self.running_queue) and not any(self.io_devices) and not self.ready_queue and not self.waiting_queue and self.api.jobs_left(session_id) == len(self.terminated_jobs):
                self.logger.info("All jobs completed!")
                break

            clock += 1

        # Calculate and log metrics
        avg_turnaround, avg_waiting, cpu_utilization = self.metrics.calculate()
        cpu_utilization = (self.cpu_busy_time / (self.metrics.total_time * len(self.running_queue))) * 100
        self.logger.info(f"Average Turnaround Time: {avg_turnaround}")
        self.logger.info(f"Average Waiting Time: {avg_waiting}")
        self.logger.info(f"CPU Utilization: {cpu_utilization:.2f}%")

        # Log turnaround time and waiting time for each job
        self.logger.info("Job Turnaround and Waiting Times:")
        for job_id, data in self.job_data.items():
            turnaround_time = data["completion_time"] - data["arrival_time"]
            waiting_time = turnaround_time - data["total_burst_time"]
            self.logger.info(f"Job {job_id} - Turnaround Time: {turnaround_time}, Waiting Time: {waiting_time}")
