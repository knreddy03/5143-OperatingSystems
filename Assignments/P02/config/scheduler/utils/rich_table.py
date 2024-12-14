from rich.table import Table
from rich.live import Live
from rich.console import Console
from rich import box
import time

class RichTable:
    def __init__(self):
        """Initialize the RichTable for live visualization."""
        self.terminal_width = Console().width
        self.live = Live(self.generate_table([], [], [], [], []), refresh_per_second=10)
        self.live.start()
        self.ready_queue = []
        self.waiting_queue = []
        self.running_cpus = []
        self.io_queue = []
        self.terminated_jobs = []

    def update(self, ready_queue, waiting_queue, running_cpus, io_queue, terminated_jobs):
        """Update the internal state for the queues and CPUs."""
        self.ready_queue = ready_queue
        self.waiting_queue = waiting_queue
        self.running_cpus = running_cpus
        self.io_queue = io_queue
        self.terminated_jobs = terminated_jobs

    def show_tables(self, ready_queue, waiting_queue, running_cpus, io_queue, terminated_jobs):
        """Render and display the updated table in the live view."""
        self.update(ready_queue, waiting_queue, running_cpus, io_queue, terminated_jobs)
        self.live.update(self.generate_table(ready_queue, waiting_queue, running_cpus, io_queue, terminated_jobs))
        time.sleep(0.05)

    def show_message(self, message):
        """Add a custom message to the visualization."""
        table = self.generate_table(
            self.ready_queue, self.waiting_queue, self.running_cpus, self.io_queue, self.terminated_jobs
        )
        table.add_row("Message", message, style="bold green", end_section=False)
        self.live.update(table)
        time.sleep(0.05)

    def make_row(self, queue_name, queue_items):
        """Create a table row for a specific queue."""
        if isinstance(queue_items, list) and all(isinstance(item, dict) for item in queue_items):
            processes = ", ".join(
                f"[bold magenta]Job{item['job_id']}[/bold magenta]" for item in queue_items
            )
        elif isinstance(queue_items, list) and all(isinstance(item, str) for item in queue_items):
            processes = ", ".join(f"[bold blue]{item}[/bold blue]" for item in queue_items)
        else:
            processes = "[dim]None[/dim]"
        return [f"[bold yellow]{queue_name}[/bold yellow]", processes]

    def generate_table(self, ready_queue, waiting_queue, running_cpus, io_queue, terminated_jobs):
        """Generate the table for visualization."""
        table = Table(box=box.HEAVY, show_header=False, title="[bold cyan]System Queues Visualization[/bold cyan]")
        table.add_column("Queue", style="bold white", width=int(self.terminal_width * 0.3))
        table.add_column("Processes", style="bold white", width=int(self.terminal_width * 0.7))

        table.add_row(*self.make_row("Ready Queue", ready_queue), end_section=True)
        table.add_row(
            "[bold yellow]Running CPUs[/bold yellow]",
            ", ".join(
                f"[bold green]CPU {cpu['cpu_id']} [Job: [bold magenta]{cpu['job']['job_id']}[/bold magenta], Remaining: {cpu['remaining_time']}[/bold green]]"
                if cpu and cpu.get("job") else f"[dim]CPU {i} [Idle][/dim]"
                for i, cpu in enumerate(running_cpus)
            ),
            end_section=True,
        )
        table.add_row(*self.make_row("Waiting Queue", waiting_queue), end_section=True)
        table.add_row(
            "[bold yellow]I/O Queue[/bold yellow]",
            ", ".join(
                f"[bold red]I/O {io['io_id']} [Job: [bold magenta]{io['job']['job_id']}[/bold magenta], Remaining: {io['remaining_time']}][/bold red]"
                if io and io.get("job") else f"[dim]I/O {i} [Idle][/dim]"
                for i, io in enumerate(io_queue)
            ),
            end_section=True,
        )
        table.add_row(*self.make_row("Terminated Jobs", terminated_jobs), end_section=True)

        return table
