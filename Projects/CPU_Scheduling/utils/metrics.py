class Metrics:
    def __init__(self):
        self.total_turnaround_time = 0
        self.total_waiting_time = 0
        self.jobs_count = 0
        self.cpu_busy_time = 0
        self.clock = 0

    def add_job_stats(self, turnaround_time, waiting_time):
        self.total_turnaround_time += turnaround_time
        self.total_waiting_time += waiting_time
        self.jobs_count += 1

    def update_cpu_busy(self):
        self.cpu_busy_time += 1

    def calculate(self):
        avg_turnaround_time = self.total_turnaround_time / self.jobs_count if self.jobs_count > 0 else 0
        avg_waiting_time = self.total_waiting_time / self.jobs_count if self.jobs_count > 0 else 0
        cpu_utilization = (self.cpu_busy_time / self.clock) * 100 if self.clock > 0 else 0
        return avg_turnaround_time, avg_waiting_time, cpu_utilization
