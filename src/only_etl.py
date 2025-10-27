from rich.console import Console

from services.etl import ServiceETL
from services.log import ServiceLog

console = Console()


def main() -> None:
    """Run only the ETL."""
    console.print("[bold yellow]running etl scripts...")
    ServiceETL.process()


if __name__ == "__main__":
    main()
