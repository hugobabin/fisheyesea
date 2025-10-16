"""Service to orchestrate ETL operations."""

import os

from etl.api import extract as api_extract
from etl.api import load as api_load
from etl.mongo import extract as mongo_extract
from etl.mongo import load as mongo_load
from etl.mongo import transform as mongo_transform
from services.log import ServiceLog


class ServiceETL:
    """ServiceETL."""

    @staticmethod
    def webscrap(disabled: bool = False):
        """Handle Webscraping ETL engine."""
        pass

    @staticmethod
    def csv(disabled: bool = False):
        """Handle CSV ETL engine."""
        pass

    @staticmethod
    def api(disabled: bool = False) -> None:
        """Handle API ETL engine."""
        if disabled:
            return
        data = api_extract()
        if data is None:
            return
        ServiceLog.console("bold yellow", "[ETL/API] extracted data")
        loaded = api_load(data)
        if loaded is None:
            return
        msg = f"[ETL/API] loaded {loaded} entries into mongo"
        ServiceLog.console("bold yellow", msg)

    @staticmethod
    def mongo(disabled: bool = False) -> None:
        """Handle Mongo ETL engine."""
        if disabled:
            return
        data = mongo_extract()
        if data is None:
            return
        ServiceLog.console("bold yellow", "[ETL/MONGO] extracted data")
        transformed = mongo_transform(data)
        if transformed is None:
            return
        loaded = mongo_load(transformed)
        if loaded is None:
            return
        msg = f"[ETL/MONGO] loaded {loaded} entries into duckdb"
        ServiceLog.console("bold yellow", msg)

    @staticmethod
    def process():
        """Handle complete ETL process."""
        etl_api_disabled = os.getenv("ETL_API_DISABLED", "false").lower() == "true"
        etl_mongo_disabled = os.getenv("ETL_MONGO_DISABLED", "false").lower() == "true"
        # etl_api_disabled = os.getenv("ETL_API_DISABLED", "false").lower() == "true"
        # etl_api_disabled = os.getenv("ETL_API_DISABLED", "false").lower() == "true"
        # etl_api_disabled = os.getenv("ETL_API_DISABLED", "false").lower() == "true"
        ServiceETL.api(etl_api_disabled)
        ServiceETL.mongo(etl_mongo_disabled)
        ServiceLog.console("bold green", "[ETL] process done")
