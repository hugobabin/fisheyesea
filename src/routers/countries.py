"""Router for Countries."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from services.jwt import get_current_user

from models.country import (
    Country,
    CountryData,
    FisheryProductionPerYear,
    PopulationPerYear,
    SeafoodConsumptionPerCapitaPerYear,
)
from services.db.maria import ServiceMaria

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=List[Country])
async def get_countries(user: dict = Depends(get_current_user)):
    """GET /countries — Retrieve all countries."""
    cur = ServiceMaria.get_cursor()
    cur.execute("SELECT code, label FROM country;")
    rows = cur.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No countries found")

    countries = [Country(code=row[0], label=row[1]) for row in rows]
    return countries


@router.get("/{code}", response_model=CountryData)
async def get_country_data(code: str, user: dict = Depends(get_current_user)):
    """GET /countries/{code} — Retrieve aggregated data for a specific country."""
    cur = ServiceMaria.get_cursor()

    # Fetch base country
    cur.execute("SELECT code, label FROM country WHERE code = %s;", (code,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Country '{code}' not found")
    country = Country(code=row[0], label=row[1])

    # Population
    cur.execute(
        "SELECT id, year, country_code, population FROM population_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    population = [
        PopulationPerYear(id=r[0], year=r[1], country_code=r[2], population=r[3])
        for r in cur.fetchall()
    ]

    # Fishery production
    cur.execute(
        "SELECT id, year, country_code, production FROM fishery_production_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    fishery = [
        FisheryProductionPerYear(id=r[0], year=r[1], country_code=r[2], production=r[3])
        for r in cur.fetchall()
    ]

    # Seafood consumption
    cur.execute(
        "SELECT id, year, country_code, consumption FROM seafood_consumption_per_capita_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    seafood = [
        SeafoodConsumptionPerCapitaPerYear(
            id=r[0], year=r[1], country_code=r[2], consumption=r[3]
        )
        for r in cur.fetchall()
    ]

    return CountryData(
        country=country,
        population=population,
        fishery_production=fishery,
        seafood_consumption=seafood,
    )


@router.get("/{code}/population", response_model=List[PopulationPerYear])
async def get_country_population(code: str, user: dict = Depends(get_current_user)):
    """GET /countries/{code}/population — Retrieve population history for a country."""
    cur = ServiceMaria.get_cursor()
    cur.execute(
        "SELECT id, year, country_code, population FROM population_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail=f"No population data for {code}")
    return [
        PopulationPerYear(id=r[0], year=r[1], country_code=r[2], population=r[3])
        for r in rows
    ]


@router.get("/{code}/fishery", response_model=List[FisheryProductionPerYear])
async def get_country_fishery(code: str, user: dict = Depends(get_current_user)):
    """GET /countries/{code}/fishery — Retrieve fishery production history for a country."""
    cur = ServiceMaria.get_cursor()
    cur.execute(
        "SELECT id, year, country_code, production FROM fishery_production_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail=f"No fishery data for {code}")
    return [
        FisheryProductionPerYear(id=r[0], year=r[1], country_code=r[2], production=r[3])
        for r in rows
    ]


@router.get("/{code}/seafood", response_model=List[SeafoodConsumptionPerCapitaPerYear])
async def get_country_seafood(code: str, user: dict = Depends(get_current_user)):
    """GET /countries/{code}/seafood — Retrieve seafood consumption history for a country."""
    cur = ServiceMaria.get_cursor()
    cur.execute(
        "SELECT id, year, country_code, consumption FROM seafood_consumption_per_capita_per_year WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail=f"No seafood data for {code}")
    return [
        SeafoodConsumptionPerCapitaPerYear(
            id=r[0], year=r[1], country_code=r[2], consumption=r[3]
        )
        for r in rows
    ]
