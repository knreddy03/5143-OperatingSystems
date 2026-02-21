from rich.table import Table
from rich.live import Live
from rich.console import Console
import time


class MLFQRichTable:
    def __init__(self):
        """Initialize the RichTable for MLFQ live visualization."""
        self.console_width = Console().width
        self.live = Live(self.generate_table([], [], []), refresh_per_second=10)
        self.live.start()
        self.queues = []
        self.running_jobs = []
        self.terminated_jobs = []

    def update(self, queues, running_jobs, terminated_jobs):
        """Update the internal state for the queues and resources."""
        self.queues = queues
        self.running_jobs = running_jobs
        self.terminated_jobs = terminated_jobs

    def show_tables(self, queues, running_jobs, terminated_jobs):
        """Render and display the updated table in the live view."""
        self.update(queues, running_jobs, terminated_jobs)
        self.live.update(self.generate_table(queues, running_jobs, terminated_jobs))
        time.sleep(0.05)

    def generate_table(self, queues, running_jobs, terminated_jobs):
        """Generate the visualization table."""
        table = Table(show_header=False, expand=True)
        table.add_column("Component", style="bold cyan", width=int(self.console_width * 0.2))
        table.add_column("Details", style="bold yellow", width=int(self.console_width * 0.8))

        # Add Multi-level Queues
        for i, queue in enumerate(queues):
            queue_name = f"Queue {i + 1}"
            queue_details = ", ".join(queue) if queue else "[Empty]"
            table.add_row(queue_name, queue_details, end_section=True)

        # Add Running CPUs
        running_details = "\n".join(running_jobs) if running_jobs else "[None]"
        table.add_row("Running CPUs", running_details, end_section=True)

        # Add Terminated Jobs
        terminated_details = ", ".join(terminated_jobs) if terminated_jobs else "[None]"
        table.add_row("Terminated Jobs", terminated_details, end_section=True)

        return table
