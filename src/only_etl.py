from services.etl import ServiceETL
from services.log import ServiceLog


def main() -> None:
    """Run only the ETL."""
    ServiceLog.console("bold yellow", "running etl scripts...")
    ServiceETL.process()


if __name__ == "__main__":
    main()
