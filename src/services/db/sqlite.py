"""Service for handling MongoDB operations."""

import sqlite3
from pathlib import Path

import pandas as pd

SQLITE_PATH = Path("../data/fisheyesea.db")


class ServiceSqlite:
    """ServiceSqlite."""

    @staticmethod
    def import_data(table_name: str, data: pd.DataFrame) -> None:
        """Import data into SQLite."""
        con = sqlite3.connect(SQLITE_PATH)
        data.to_sql(name=table_name, con=con, if_exists="replace")

    @staticmethod
    def clean_data() -> None:
        """Clean data in SQLite."""
        if SQLITE_PATH.exists():
            SQLITE_PATH.unlink()

    @staticmethod
    def get_data(table_name: str, columns: list[str]) -> pd.DataFrame:
        """Get data from SQLite."""
        con = sqlite3.connect(SQLITE_PATH)
        columns = ", ".join(columns)
        query = "SELECT %s FROM %s" % (columns, table_name)
        return pd.read_sql_query(sql=query, con=con)
