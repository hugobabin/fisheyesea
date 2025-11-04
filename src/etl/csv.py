import io
import zipfile
from pathlib import Path

import httpx
import pandas as pd

from services.db.sqlite import ServiceSqlite
from services.log import ServiceLog
from services.util import ServiceUtil

CSV_SEAFOOD_CONSUMPTION_URL = "https://ourworldindata.org/grapher/fish-and-seafood-consumption-per-capita.csv?v=1&csvType=full&useColumnShortNames=false"
CSV_FISHERIES_PRODUCTION_URL = (
    "https://api.worldbank.org/v2/en/indicator/ER.FSH.CAPT.MT?downloadformat=csv"
)
CSV_FISHERIES_PRODUCTION_NAME = "API_ER.FSH.CAPT.MT_DS2_en_csv_v2_6149.csv"

CSV_POPULATION = Path("../data/population-by-country-2022.csv")
CSV_FISHERIES_PRODUCTION = Path("../data/API_ER.FSH.CAPT.MT_DS2_en_csv_v2_6149.csv")
CSV_SEAFOOD_CONSUMPTION = Path("../data/fish-and-seafood-consumption-per-capita.csv")


def extract_population() -> pd.DataFrame:
    """Extract data from CSV_POPULATION."""
    if CSV_POPULATION.exists() is not True:
        ServiceLog.console("bold red", "[ETL/CSV] can't find CSV_POPULATION")
        return None
    try:
        return pd.read_csv(CSV_POPULATION)
    except Exception as exc:
        ServiceLog.console(
            "bold red", "[ETL/CSV] error when converting CSV_POPULATION to DataFrame"
        )
        ServiceLog.console("bold red", f"[ETL/CSV] error is {str(exc)}")
        return None


def extract_fisheries_production() -> pd.DataFrame:
    """Extract data from CSV_FISHERIES_PRODUCTION."""
    if CSV_FISHERIES_PRODUCTION.exists() is not True:
        ServiceLog.console("bold red", "[ETL/CSV] can't find CSV_FISHERIES_PRODUCTION")
        ServiceLog.console(
            "bold yellow", "[ETL/CSV] downloading CSV_FISHERIES_PRODUCTION"
        )
        r = httpx.get(CSV_FISHERIES_PRODUCTION_URL)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extract(CSV_FISHERIES_PRODUCTION_NAME, "../data")
        ServiceLog.console(
            "bold yellow", "[ETL/CSV] downloaded CSV_FISHERIES_PRODUCTION"
        )
    try:
        return pd.read_csv(CSV_FISHERIES_PRODUCTION, skiprows=4)
    except Exception as exc:
        ServiceLog.console(
            "bold red",
            "[ETL/CSV] error when converting CSV_FISHERIES_PRODUCTION to DataFrame",
        )
        ServiceLog.console("bold red", f"[ETL/CSV] error is {str(exc)}")
        return None


def extract_seafood_consumption() -> pd.DataFrame:
    """Extract data from CSV_SEAFOOD_CONSUMPTION."""
    if CSV_SEAFOOD_CONSUMPTION.exists() is not True:
        ServiceLog.console("bold red", "[ETL/CSV] can't find CSV_SEAFOOD_CONSUMPTION")
        ServiceLog.console(
            "bold yellow", "[ETL/CSV] downloading CSV_SEAFOOD_CONSUMPTION"
        )
        r = httpx.get(CSV_SEAFOOD_CONSUMPTION_URL)
        r.raise_for_status()
        with CSV_SEAFOOD_CONSUMPTION.open("wb") as f:
            f.write(r.content)
        ServiceLog.console(
            "bold yellow", "[ETL/CSV] downloaded CSV_SEAFOOD_CONSUMPTION"
        )
    try:
        return pd.read_csv(CSV_SEAFOOD_CONSUMPTION)
    except Exception as exc:
        ServiceLog.console(
            "bold red",
            "[ETL/CSV] error when converting CSV_SEAFOOD_CONSUMPTION to DataFrame",
        )
        ServiceLog.console("bold red", f"[ETL/CSV] error is {str(exc)}")
        return None


def transform_population(df: pd.DataFrame) -> pd.DataFrame:
    """Transform CSV_POPULATION data."""
    df_final = df[["Country_Name", "Country_Population"]].copy()
    df_final["Country_Name"] = df_final["Country_Name"].apply(
        ServiceUtil.get_country_code
    )
    df_final = df_final.rename(columns={"Country_Name": "Country_Code"})
    df_final = df_final.dropna()
    df_final["Country_Population"] = df_final["Country_Population"].str.replace(",", "")
    df_final["Country_Population"] = df_final["Country_Population"].astype("int32")
    return df_final


def transform_fisheries_production(df: pd.DataFrame) -> list[dict]:
    """Transform CSV_FISHERIES_PRODUCTION data."""
    df_final = df[["Country Code", "2022"]]
    df_final = df_final.dropna()
    return df_final.rename(
        columns={
            "Country Code": "Country_Code",
            "2022": "Country_Fishery_Production",
        }
    )


def transform_seafood_consumption(df: pd.DataFrame) -> list[dict]:
    """Transform CSV_SEAFOOD_CONSUMPTION data."""
    seafood_consumption_column = "Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita"
    df_final = df.loc[df["Year"] == 2022, ["Code", seafood_consumption_column]]
    df_final = df_final.rename(
        columns={
            seafood_consumption_column: "Country_Seafood_Consumption_Per_Capita",
            "Code": "Country_Code",
        },
    )
    return df_final.dropna()


def load_fisheries_production(df: pd.DataFrame) -> int | None:
    """Load CSV_FISHERIES_PRODUCTION data into sqlite."""
    try:
        ServiceSqlite.import_data("country_fishery_production", df)
    except Exception as exc:
        ServiceLog.console(
            "bold red",
            "[ETL/CSV] error when importing CSV_FISHERIES_PRODUCTION into sqlite",
        )
        msg = f"[ETL/CSV] error is {str(exc)}"
        ServiceLog.console("bold red", msg)
        return None
    return len(df)


def load_population(df: pd.DataFrame) -> int | None:
    """Load CSV_POPULATION data into sqlite."""
    try:
        ServiceSqlite.import_data("country_population", df)
    except Exception as exc:
        ServiceLog.console(
            "bold red",
            "[ETL/CSV] error when importing CSV_POPULATION into sqlite",
        )
        msg = f"[ETL/CSV] error is {str(exc)}"
        ServiceLog.console("bold red", msg)
        return None
    return len(df)


def load_seafood_consumption(df: pd.DataFrame) -> int | None:
    """Load CSV_SEAFOOD_CONSUMPTION data into sqlite."""
    try:
        ServiceSqlite.import_data("country_seafood_consumption_per_capita", df)
    except Exception as exc:
        ServiceLog.console(
            "bold red",
            "[ETL/CSV] error when importing CSV_SEAFOOD_CONSUMPTION into sqlite",
        )
        msg = f"[ETL/CSV] error is {str(exc)}"
        ServiceLog.console("bold red", msg)
        return None
    return len(df)
