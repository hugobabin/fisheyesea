"""Service for handling utility functions."""

import os

import pycountry
from dotenv import load_dotenv

from services.log import ServiceLog

ISO_3166_ALPHA_3 = {
    # ENUM containing iso 3166 alpha 3 codes.
    # For handling missing codes with get_country_code function.
    "congo": "COG",
    "iran": "IRN",
    "venezuela": "VEN",
    "people's republic of korea": "PRK",
    "taiwan province of china": "TWN",
    "bolivia": "BOL",
    "hong kong sar": "HKG",
    "kosovo": "XKX",
    "macao sar": "MAC",
    "micronesia": "FSM",
    "united states virgin islands": "VIR",
    "wallis and futuna islands": "WLF",
}


def get_country_code_with_enum(country_name: str) -> str | None:
    """Get country code for country which country code has not been found through standard means."""
    country_name = str.lower(country_name)
    for key in ISO_3166_ALPHA_3:
        if key in country_name:
            return ISO_3166_ALPHA_3[key]
    return None


class ServiceUtil:
    """ServiceUtil."""

    @staticmethod
    def get_env(key: str, fallback: str) -> str:
        """Get environment variable."""
        load_dotenv("../config/.env")
        return os.getenv(key, fallback)

    @staticmethod
    def get_country_code(name: str) -> str | None:
        """Get country iso3166 code by name using fuzzy search."""
        try:
            results = pycountry.countries.search_fuzzy(name)
            return results[0].alpha_3
        except Exception:
            # fallback
            country_code = get_country_code_with_enum(name)
            if country_code is not None:
                return country_code
            ServiceLog.console("bold red", f"[UTIL] can't find iso3166 code for {name}")
            return None
