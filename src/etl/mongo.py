import duckdb
import pandas as pd

from services.db.duck import ServiceDuck
from services.db.mongo import ServiceMongo
from services.log import ServiceLog


def extract() -> list[dict] | None:
    """Extract Mongo data."""
    data = ServiceMongo.get_data()

    if not isinstance(data, list) or len(data) == 0:
        ServiceLog.console(
            "bold red",
            "[ETL/MONGO] no data to retrieve",
        )
        return None

    return data


def transform(data: list[dict]) -> pd.DataFrame:
    """Transform data extracted from Mongo."""
    df = pd.DataFrame(data)
    df_final = pd.DataFrame()

    def extract_coords(pos: dict) -> tuple:
        """Extract latitude and longitude from pos."""
        lat = pos["lat"]
        lon = pos["lon"]
        return lat, lon

    df_final[["lat", "lon"]] = df["position"].apply(
        lambda pos: pd.Series(extract_coords(pos)),
    )
    df_final[["start", "end"]] = df[["start", "end"]]

    return df_final


def load(data: pd.DataFrame) -> None:
    """Load Mongo data into DuckDB after cleaning existing data."""
    entries = data.count().max()
    try:
        ServiceDuck.connect()
    except Exception:  # noqa: BLE001
        ServiceLog.console(
            "bold red",
            "[ETL/MONGO] error during connection to duckdb",
        )
        return None
    try:
        ServiceDuck.import_data(data)
    except Exception as exc:  # noqa: BLE001
        print(exc)
        ServiceLog.console(
            "bold red",
            "[ETL/MONGO] error when loading data into duckdb",
        )
        return None
    return entries
