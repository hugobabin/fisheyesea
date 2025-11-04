import json
from io import StringIO
from pathlib import Path

import httpx
import pandas as pd
from selectolax.lexbor import LexborHTMLParser as HTMLParser

from services.log import ServiceLog

STATUS_CODE_OK = 200

URL = "https://database.earth/population/by-country/2022"

ROOT = "https://database.earth/"

CACHE_PATH = Path("../data/population-by-country-2022.html")
CSV_PATH = Path("../data/population-by-country-2022.csv")


def get_cached_file() -> str:
    """Get cached HTML if it exists."""
    if CACHE_PATH.exists():
        return CACHE_PATH.read_text(encoding="utf-8")
    return None


def extract() -> str:
    """Extract data from {URL}."""
    cached_content = get_cached_file()
    if cached_content is not None:
        return cached_content
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Referer": ROOT,
    }
    res = httpx.get(url=URL, headers=headers, timeout=60)
    if res.status_code != STATUS_CODE_OK:
        msg = f"[ETL/WEBSCRAP] failure in extract/httpx.get POPULATION - status code is {res.status_code}"
        ServiceLog.console("bold red", msg)
        msg = f"[ETL/WEBSCRAP] error is {res.content}"
        ServiceLog.console("bold red", msg)
        return None
    data = res.text
    CACHE_PATH.write_text(data, encoding="utf-8")
    return data


def transform(data: str) -> list[dict]:
    """Transform webscrapped data."""
    tree = HTMLParser(data)
    # country_rows = tree.css("bg-gray-100")
    country_rows = [
        tr
        for tr in tree.css("tr")
        if tr.attributes.get("class") == "even:bg-white odd:bg-gray-100"
    ]
    countries = []
    for country_row in country_rows:
        country_name = country_row.css_first("a").text()
        country_population = country_row.css_first("td:not(:has(a))").text()
        country = {
            "Country_Name": country_name,
            "Country_Population": country_population,
        }
        countries.append(country)
    return countries


def load(data: list[dict]) -> None:
    """Load webscrapped data in a CSV file."""
    entries = len(data)
    data = StringIO(json.dumps(data))
    df = pd.read_json(data)
    df.to_csv(CSV_PATH)
    return entries
