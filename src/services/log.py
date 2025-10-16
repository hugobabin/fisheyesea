"""Service for handling logs."""

import logging

from rich.console import Console

rich_console = Console()


class ServiceLog:
    """ServiceLog."""

    @staticmethod
    def info(msg: str) -> None:
        """Send a log at INFO level."""
        logger = logging.getLogger("uvicorn.access")
        msg = f"[bold green] 🐟​ {msg}"
        logger.info(msg=msg)

    @staticmethod
    def error(msg: str) -> None:
        """Send a log at ERROR level."""
        logger = logging.getLogger("uvicorn.error")
        msg = f"[bold red] 💀 {msg}"
        logger.error(msg=msg)

    @staticmethod
    def console(color: str, msg: str) -> None:
        """Send a console message without using logging."""
        msg = f"[{color}]{msg}"
        rich_console.print(msg)
