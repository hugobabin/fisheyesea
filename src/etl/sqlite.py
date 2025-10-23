import pandas as pd

from services.db.maria import ServiceMaria
from services.db.sqlite import ServiceSqlite
from services.log import ServiceLog


def extract() -> tuple[pd.DataFrame]:
    """Extract data from sqlite."""
    df_fishery_production = ServiceSqlite.get_data("country_fishery_production")
    df_population = ServiceSqlite.get_data("country_population")
    df_seafood_consumption = ServiceSqlite.get_data(
        "country_seafood_consumption_per_capita"
    )
    return (df_fishery_production, df_population, df_seafood_consumption)


def transform(data: tuple[pd.DataFrame]) -> pd.DataFrame:
    """Transform data extracted from Mongo."""
    df_fishery_production, df_population, df_seafood_consumption = data
    df_fishery_production = df_fishery_production.drop(columns=["index"])
    df_population = df_population.drop(columns=["index"])
    df_seafood_consumption = df_seafood_consumption.drop(columns=["index"])
    common_codes = (
        set(df_fishery_production["Country_Code"])
        & set(df_population["Country_Code"])
        & set(df_seafood_consumption["Country_Code"])
    )
    return (
        df_fishery_production[df_fishery_production["Country_Code"].isin(common_codes)]
        .merge(df_population, on="Country_Code")
        .merge(df_seafood_consumption, on="Country_Code")
    )


def create_database(cur) -> None:
    """Create/replace tables."""
    query_fishery_production_per_year = """
        CREATE OR REPLACE TABLE fishery_production_per_year (
            year YEAR PRIMARY KEY NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            production INT UNSIGNED DEFAULT 0
        );
    """
    query_seafood_consumption_per_capita_per_year = """
        CREATE OR REPLACE TABLE seafood_consumption_per_capita_per_year (
            year YEAR PRIMARY KEY NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            consumption INT UNSIGNED DEFAULT 0
        );
    """
    query_population_per_year = """
        CREATE OR REPLACE TABLE population_per_year (
            year YEAR PRIMARY KEY NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            population INT UNSIGNED DEFAULT 0
        );
    """
    query_country = """
        CREATE OR REPLACE TABLE country (
            code VARCHAR(3) PRIMARY KEY NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            label VARCHAR(128) DEFAULT "Undefined Country"
        );
    """
    query_constraint_fishery = """
        ALTER TABLE fishery_production_per_year
        ADD CONSTRAINT fk_country_fishery
        FOREIGN KEY (country_code) REFERENCES country(code);
    """
    query_constraint_seafood = """
        ALTER TABLE seafood_consumption_per_capita_per_year
        ADD CONSTRAINT fk_country_seafood
        FOREIGN KEY (country_code) REFERENCES country(code);
    """
    query_constraint_population = """
        ALTER TABLE population_per_year
        ADD CONSTRAINT fk_country_population
        FOREIGN KEY (country_code) REFERENCES country(code);
    """
    cur.execute(query_fishery_production_per_year)
    cur.execute(query_seafood_consumption_per_capita_per_year)
    cur.execute(query_population_per_year)
    cur.execute(query_country)
    cur.execute(query_constraint_fishery)
    cur.execute(query_constraint_seafood)
    cur.execute(query_constraint_population)


def load(data: pd.DataFrame) -> None:
    """Load data into MariaDB."""
    cur = ServiceMaria.get_cursor()
    create_database(cur)
