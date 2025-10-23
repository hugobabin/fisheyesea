"""Models for describing country-related data."""

from datetime import date

from pydantic import BaseModel, Field


class Country(BaseModel):
    """Country entity."""

    code: str = Field(
        ..., min_length=3, max_length=3, description="ISO 3166-1 alpha-3 country code"
    )
    label: str = Field(default="Undefined Country", description="Country name or label")


class FisheryProductionPerYear(BaseModel):
    """Annual fishery production per country."""

    id: int | None = None
    year: int = Field(..., ge=1900, le=date.today().year)
    country_code: str = Field(..., min_length=3, max_length=3)
    production: int = Field(
        default=0, ge=0, description="Total fishery production in metric tons"
    )


class SeafoodConsumptionPerCapitaPerYear(BaseModel):
    """Annual seafood consumption per capita per country."""

    id: int | None = None
    year: int = Field(..., ge=1900, le=date.today().year)
    country_code: str = Field(..., min_length=3, max_length=3)
    consumption: float = Field(
        default=0.0, ge=0.0, description="Seafood consumption per capita (kg/year)"
    )


class PopulationPerYear(BaseModel):
    """Annual population per country."""

    id: int | None = None
    year: int = Field(..., ge=1900, le=date.today().year)
    country_code: str = Field(..., min_length=3, max_length=3)
    population: int = Field(
        default=0, ge=0, description="Population count for the given year"
    )


class CountryData(BaseModel):
    """Aggregated model combining all available data for a country."""

    country: Country
    population: list[PopulationPerYear] = []
    fishery_production: list[FisheryProductionPerYear] = []
    seafood_consumption: list[SeafoodConsumptionPerCapitaPerYear] = []
