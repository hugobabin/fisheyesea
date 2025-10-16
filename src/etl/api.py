import json

import httpx

from services.db.mongo import ServiceMongo
from services.log import ServiceLog
from services.util import ServiceUtil

STATUS_CODE_OK = 200

API_LIMIT = 500
API_OFFSET = 0

API_URL = f"https://gateway.api.globalfishingwatch.org/v3/events?datasets[0]=public-global-fishing-events:latest&start-date=2017-01-01&end-date=2024-12-31&limit={API_LIMIT}&offset={API_OFFSET}"
API_TOKEN = ServiceUtil.get_env("API_TOKEN", "undefined")


def extract() -> bytes | None:
    """Extract API data."""
    if API_TOKEN == "undefined":  # noqa: S105
        msg = "[ETL/API] can't retrieve API_TOKEN - please set it in your .env"
        ServiceLog.console("bold red", msg)
        return None
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }
    res = httpx.get(url=API_URL, headers=headers, timeout=360)
    if res.status_code != STATUS_CODE_OK:
        msg = (
            f"[ETL/API] failure in extract/httpx.get - status code is {res.status_code}"
        )
        ServiceLog.console("bold red", msg)
        msg = f"[ETL/API] error is {res.content}"
        ServiceLog.console("bold red", msg)
        return None
    return res.content


def load(data: bytes) -> None:
    """Load API data in Mongo after cleaning already existing data."""
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        ServiceLog.console("bold red", "[ETL/API] failed to parse JSON")
        return None

    fishing_efforts = list(json_data.get("entries", []))

    if not isinstance(fishing_efforts, list) or len(fishing_efforts) == 0:
        ServiceLog.console("bold red", "[ETL/API] no data to insert into Mongo")
        return None
    ServiceMongo.clean_data()
    ServiceMongo.import_data(fishing_efforts)
    return len(fishing_efforts)
