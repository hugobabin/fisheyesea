"""Service for handling utility functions."""

import os

from dotenv import load_dotenv


class ServiceUtil:
    """ServiceUtil."""

    @staticmethod
    def get_env(key: str, fallback: str) -> str:
        """Get environment variable."""
        load_dotenv("../config/.env")
        return os.getenv(key, fallback)
