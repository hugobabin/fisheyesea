"""Service to orchestrate ETL operations."""

import os

from etl import api, csv, mongo, sqlite, webscrap
from services.db.sqlite import ServiceSqlite
from services.log import ServiceLog


class ServiceETL:
    """ServiceETL."""

    @staticmethod
    def webscrap(disabled: bool = False) -> None:
        """Handle Webscraping ETL engine."""
        if disabled:
            return
        data = webscrap.extract()
        if data is None:
            return
        ServiceLog.console(
            "bold yellow",
            "[ETL/WEBSCRAP] extracted data about population",
        )
        transformed = webscrap.transform(data)
        if transformed is None:
            return
        loaded = webscrap.load(transformed)
        if loaded is None:
            return
        msg = f"[ETL/WEBSCRAP] loaded {loaded} entries into CSV"
        ServiceLog.console("bold yellow", msg)

    @staticmethod
    def csv_population(disabled: bool = False) -> None:
        """Handle CSV ETL engine."""
        if disabled:
            return
        data = csv.extract_population()
        if data is None:
            return
        ServiceLog.console(
            "bold yellow",
            "[ETL/CSV] extracted data from CSV_POPULATION",
        )
        transformed = csv.transform_population(data)
        if transformed is None:
            return
        loaded = csv.load_population(transformed)
        if loaded is None:
            return
        ServiceLog.console(
            "bold yellow",
            f"[ETL/CSV] loaded {loaded} entries from CSV_POPULATION data into sqlite",
        )

    @staticmethod
    def csv_fisheries_production(disabled: bool = False) -> None:
        """Handle CSV ETL engine."""
        if disabled:
            return
        data = csv.extract_fisheries_production()
        if data is None:
            return
        ServiceLog.console(
            "bold yellow",
            "[ETL/CSV] extracted data from CSV_FISHERIES_PRODUCTION",
        )
        transformed = csv.transform_fisheries_production(data)
        if transformed is None:
            return
        loaded = csv.load_fisheries_production(transformed)
        if loaded is None:
            return
        ServiceLog.console(
            "bold yellow",
            f"[ETL/CSV] loaded {loaded} entries from CSV_FISHERIES_PRODUCTION data into sqlite",
        )

    @staticmethod
    def csv_seafood_consumption(disabled: bool = False) -> None:
        """Handle CSV ETL engine."""
        if disabled:
            return
        data = csv.extract_seafood_consumption()
        if data is None:
            return
        ServiceLog.console(
            "bold yellow",
            "[ETL/CSV] extracted data from CSV_SEAFOOD_CONSUMPTION",
        )
        transformed = csv.transform_seafood_consumption(data)
        if transformed is None:
            return
        loaded = csv.load_seafood_consumption(transformed)
        if loaded is None:
            return
        ServiceLog.console(
            "bold yellow",
            f"[ETL/CSV] loaded {loaded} entries from CSV_SEAFOOD_CONSUMPTION data into sqlite",
        )

    @staticmethod
    def sqlite(disabled: bool = False) -> None:
        """Handle SQLite ETL engine."""
        if disabled:
            return
        data = sqlite.extract()
        if data is None:
            return
        ServiceLog.console(
            "bold yellow",
            "[ETL/SQLITE] extracted data from sqlite",
        )
        transformed = sqlite.transform(data)
        if transformed is None:
            return
        loaded = sqlite.load(transformed)
        if loaded is None:
            return
        ServiceLog.console(
            "bold yellow",
            f"[ETL/SQLITE] loaded {loaded} entries into mariadb",
        )

    @staticmethod
    def api(disabled: bool = False) -> None:
        """Handle API ETL engine."""
        if disabled:
            return
        data = api.extract()
        if data is None:
            return
        ServiceLog.console("bold yellow", "[ETL/API] extracted data")
        loaded = api.load(data)
        if loaded is None:
            return
        msg = f"[ETL/API] loaded {loaded} entries into mongo"
        ServiceLog.console("bold yellow", msg)

    @staticmethod
    def mongo(disabled: bool = False) -> None:
        """Handle Mongo ETL engine."""
        if disabled:
            return
        data = mongo.extract()
        if data is None:
            return
        ServiceLog.console("bold yellow", "[ETL/MONGO] extracted data")
        transformed = mongo.transform(data)
        if transformed is None:
            return
        loaded = mongo.load(transformed)
        if loaded is None:
            return
        msg = f"[ETL/MONGO] loaded {loaded} entries into duckdb"
        ServiceLog.console("bold yellow", msg)

    @staticmethod
    def process() -> None:
        """Handle complete ETL process."""
        etl_api_disabled = os.getenv("ETL_API_DISABLED", "false").lower() == "true"
        etl_mongo_disabled = os.getenv("ETL_MONGO_DISABLED", "false").lower() == "true"
        etl_webscrap_disabled = (
            os.getenv("ETL_WEBSCRAP_DISABLED", "false").lower() == "true"
        )
        etl_csv_disabled = os.getenv("ETL_CSV_DISABLED", "false").lower() == "true"
        etl_sqlite_disabled = (
            os.getenv("ETL_SQLITE_DISABLED", "false").lower() == "true"
        )
        ServiceETL.api(etl_api_disabled)
        ServiceETL.mongo(etl_mongo_disabled)
        ServiceETL.webscrap(etl_webscrap_disabled)
        if etl_csv_disabled is False:
            ServiceSqlite.clean_data()
        ServiceETL.csv_population(etl_csv_disabled)
        ServiceETL.csv_fisheries_production(etl_csv_disabled)
        ServiceETL.csv_seafood_consumption(etl_csv_disabled)
        ServiceETL.sqlite(etl_sqlite_disabled)
        ServiceLog.console("bold green", "[ETL] process done")
