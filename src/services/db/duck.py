"""Service for handling DuckDB operations."""

import duckdb
import pandas as pd
from duckdb import DuckDBPyConnection

from models.fishingeffort import FishingEffort

DUCKDB_PATH = "../data/fisheyesea.duckdb"


class ServiceDuck:
    """ServiceDuck."""

    con: DuckDBPyConnection = None

    @classmethod
    def connect(cls) -> None:
        """Connect to DuckDB with {DUCKDB_PATH}."""
        cls.con = duckdb.connect(DUCKDB_PATH)

    @classmethod
    def import_data(cls, data: pd.DataFrame) -> None:
        """Import data into DuckDB."""
        query = "CREATE TABLE fishing_efforts AS SELECT * FROM data"
        cls.con.sql(query)

    @classmethod
    def get_data(cls) -> list[FishingEffort]:
        """Get data from DuckDB."""
        query = "SELECT * FROM fishing_efforts"
        efforts = cls.con.sql(query).to_df().to_dict(orient="records")
        return [FishingEffort.model_validate(effort) for effort in efforts]
