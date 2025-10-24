import json
from io import StringIO
from pathlib import Path

import httpx
import pandas as pd
from selectolax.lexbor import LexborHTMLParser as HTMLParser

from services.log import ServiceLog

STATUS_CODE_OK = 200

URL_POPULATION = "https://database.earth/population/by-country/2022"
URL_FISHERIES_PRODUCTION = "https://data.worldbank.org/indicator/ER.FSH.CAPT.MT?end=2022&most_recent_value_desc=true&start=2021&view=chart"

ROOT_POPULATION = "https://database.earth/"
ROOT_FISHERIES_PRODUCTION = "https://data.worldbank.org/"

CACHE_PATH_POPULATION = Path("../data/population-by-country-2022.html")
CSV_PATH_POPULATION = Path("../data/population-by-country-2022.csv")

CACHE_PATH_FISHERIES_PRODUCTION = Path(
    "../data/fisheries-production-by-country-2022.html"
)
CSV_PATH_FISHERIES_PRODUCTION = Path("../data/population-by-country-2022.csv")


def get_cached_file_population() -> str:
    """Get cached HTML if it exists."""
    if CACHE_PATH_POPULATION.exists():
        return CACHE_PATH_POPULATION.read_text(encoding="utf-8")
    return None


def get_cached_file_fisheries_production() -> str:
    """Get cached HTML if it exists."""
    if CACHE_PATH_FISHERIES_PRODUCTION.exists():
        return CACHE_PATH_FISHERIES_PRODUCTION.read_text(encoding="utf-8")
    return None


def extract_population() -> str:
    """Extract data from {URL_POPULATION}."""
    cached_content = get_cached_file_population()
    if cached_content is not None:
        return cached_content
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Referer": ROOT_POPULATION,
    }
    res = httpx.get(url=URL_POPULATION, headers=headers, timeout=60)
    if res.status_code != STATUS_CODE_OK:
        msg = f"[ETL/WEBSCRAP] failure in extract/httpx.get POPULATION - status code is {res.status_code}"
        ServiceLog.console("bold red", msg)
        msg = f"[ETL/WEBSCRAP] error is {res.content}"
        ServiceLog.console("bold red", msg)
        return None
    data = res.text
    CACHE_PATH_POPULATION.write_text(data, encoding="utf-8")
    return data


def extract_fisheries_production() -> str:
    """Extract data from {URL_FISHERIES_PRODUCTION}."""
    cached_content = get_cached_file_fisheries_production()
    if cached_content is not None:
        return cached_content
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Referer": ROOT_FISHERIES_PRODUCTION,
    }
    res = httpx.get(url=URL_FISHERIES_PRODUCTION, headers=headers, timeout=60)
    if res.status_code != STATUS_CODE_OK:
        msg = f"[ETL/WEBSCRAP] failure in extract/httpx.get FISHERIES_PRODUCTION - status code is {res.status_code}"
        ServiceLog.console("bold red", msg)
        msg = f"[ETL/WEBSCRAP] error is {res.content}"
        ServiceLog.console("bold red", msg)
        return None
    data = res.text
    CACHE_PATH_FISHERIES_PRODUCTION.write_text(data, encoding="utf-8")
    return data


def transform_population(data: str) -> list[dict]:
    """Transform webscrapped data."""
    tree = HTMLParser(data)
    country_rows = tree.css("tr.odd\\:bg-gray-100")
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


# def transform_fisheries_production(data: str) -> list[dict]:
#     """Transform webscrapped data."""
#     tree = HTMLParser(data)
#     fisheries_production_rows = tree.css("tr.odd\\:bg-gray-100")
#     countries = []
#     for country_row in country_rows:
#         country_name = country_row.css_first("a").text()
#         country_population = country_row.css_first("td:not(:has(a))").text()
#         country = {
#             "Country_Name": country_name,
#             "Country_Population": country_population,
#         }
#         countries.append(country)
#     return countries


def load_population(data: list[dict]) -> None:
    """Load webscrapped data in a CSV file."""
    entries = len(data)
    data = StringIO(json.dumps(data))
    df = pd.read_json(data)
    df.to_csv(CSV_PATH_POPULATION)
    return entries
