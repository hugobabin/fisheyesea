import pandas as pd

from services.db.maria import ServiceMaria
from services.db.sqlite import ServiceSqlite
from services.log import ServiceLog
from services.util import ServiceUtil


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
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            year YEAR NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            production INT UNSIGNED DEFAULT 0
        );
    """
    query_seafood_consumption_per_capita_per_year = """
        CREATE OR REPLACE TABLE seafood_consumption_per_capita_per_year (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            year YEAR NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            consumption INT UNSIGNED DEFAULT 0
        );
    """
    query_population_per_year = """
        CREATE OR REPLACE TABLE population_per_year (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            year YEAR NOT NULL,
            country_code VARCHAR(3) NOT NULL,
            population INT UNSIGNED DEFAULT 0
        );
    """
    query_country = """
        CREATE OR REPLACE TABLE country (
            code VARCHAR(3) PRIMARY KEY NOT NULL,
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
    ServiceMaria.exec(query_fishery_production_per_year)
    ServiceMaria.exec(query_seafood_consumption_per_capita_per_year)
    ServiceMaria.exec(query_population_per_year)
    ServiceMaria.exec(query_country)
    ServiceMaria.exec(query_constraint_fishery)
    ServiceMaria.exec(query_constraint_seafood)
    ServiceMaria.exec(query_constraint_population)


def load(data: pd.DataFrame) -> None:
    """Load data into MariaDB."""
    cur = ServiceMaria.get_cursor()
    data["Country_Label"] = data["Country_Code"].apply(ServiceUtil.get_country_label)
    data_fishery = data[["Country_Code", "Country_Fishery_Production_2022"]].to_dict(
        orient="records"
    )
    data_seafood = data[
        ["Country_Code", "Country_Seafood_Consumption_Per_Capita"]
    ].to_dict(orient="records")
    data_population = data[["Country_Code", "Country_Population"]].to_dict(
        orient="records"
    )
    data_country = data[["Country_Code", "Country_Label"]].to_dict(orient="records")
    create_database(cur)
    for country in data_country:
        query = f"""
            INSERT INTO country (code, label)
            VALUES ('{country.get("Country_Code")}', "{country.get('Country_Label')}")
            ON DUPLICATE KEY UPDATE code = code;
        """
        ServiceMaria.exec(query)
    for fishery in data_fishery:
        query = f"""
            INSERT INTO fishery_production_per_year (year, country_code, production)
            VALUES (
                2022,
                '{fishery.get("Country_Code")}',
                {fishery.get("Country_Fishery_Production_2022")}
            )
        """
        ServiceMaria.exec(query)
    for seafood in data_seafood:
        query = f"""
            INSERT INTO seafood_consumption_per_capita_per_year (year, country_code, consumption)
            VALUES (
                2022,
                '{seafood.get("Country_Code")}',
                {seafood.get("Country_Seafood_Consumption_Per_Capita")}
            )
        """
        ServiceMaria.exec(query)
    for population in data_population:
        query = f"""
            INSERT INTO population_per_year (year, country_code, population)
            VALUES (
                2022,
                '{population.get("Country_Code")}',
                {population.get("Country_Population")}
            )
        """
        ServiceMaria.exec(query)
    return len(data)
