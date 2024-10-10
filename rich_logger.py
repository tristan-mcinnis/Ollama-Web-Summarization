from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    return logging.getLogger("rich")

def log_step(message):
    console.rule(f"[bold blue]{message}")

def log_result(message):
    console.print(f"[bold green]Result:[/bold green] {message}")

def log_error(message):
    console.print(f"[bold red]Error:[/bold red] {message}", style="red")
