"""Router for Countries and related data."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from models.country import (
    Country,
    CountryData,
    FisheryProductionPerYear,
    PopulationPerYear,
    SeafoodConsumptionPerCapitaPerYear,
)
from services.db.maria import ServiceMaria
from services.jwt import get_current_user

router = APIRouter(prefix="/countries")


def get_cursor():
    """Get a DB cursor with context management."""
    return ServiceMaria.get_cursor()


def not_found(detail: str):
    """Helper to raise a 404 HTTPException."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.get(
    "/",
    response_model=list[Country],
    tags=["Countries - General"],
)
async def get_countries(user: Annotated[dict, Depends(get_current_user)]):
    """GET /countries — Retrieve all countries."""
    cur = get_cursor()
    cur.execute("SELECT code, label FROM country;")
    rows = cur.fetchall()
    if not rows:
        not_found("No countries found")

    return [Country(code=row[0], label=row[1]) for row in rows]


@router.get("/{code}", response_model=CountryData, tags=["Countries - General"])
async def get_country_data(code: str, user: Annotated[dict, Depends(get_current_user)]):
    """GET /countries/{code} — Retrieve aggregated data for a specific country."""
    cur = get_cursor()

    # Base country
    cur.execute("SELECT code, label FROM country WHERE code = %s;", (code,))
    row = cur.fetchone()
    if not row:
        not_found(f"Country '{code}' not found")

    country = Country(code=row[0], label=row[1])

    # Population
    cur.execute(
        "SELECT id, year, country_code, population FROM population_per_year "
        "WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    population = [
        PopulationPerYear(id=r[0], year=r[1], country_code=r[2], population=r[3])
        for r in cur.fetchall()
    ]

    cur.execute(
        "SELECT id, year, country_code, production FROM fishery_production_per_year "
        "WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    fishery = [
        FisheryProductionPerYear(id=r[0], year=r[1], country_code=r[2], production=r[3])
        for r in cur.fetchall()
    ]

    cur.execute(
        "SELECT id, year, country_code, consumption FROM seafood_consumption_per_capita_per_year "
        "WHERE country_code = %s ORDER BY year;",
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


@router.get(
    "/{code}/population",
    response_model=list[PopulationPerYear],
    tags=["Countries - Population"],
)
async def get_country_population(
    code: str, user: Annotated[dict, Depends(get_current_user)]
):
    """GET /countries/{code}/population — Retrieve population history for a country."""
    cur = get_cursor()
    cur.execute(
        "SELECT id, year, country_code, population FROM population_per_year "
        "WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        not_found(f"No population data for {code}")
    return [
        PopulationPerYear(id=r[0], year=r[1], country_code=r[2], population=r[3])
        for r in rows
    ]


@router.post(
    "/{code}/population",
    status_code=status.HTTP_201_CREATED,
    tags=["Countries - Population"],
)
async def add_country_population(
    code: str,
    year: Annotated[int, Body(ge=0, le=9999)],
    population: Annotated[int, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """POST /countries/{code}/population — Add new population data."""
    cur = get_cursor()
    try:
        cur.execute(
            "INSERT INTO population_per_year (year, country_code, population) VALUES (%s, %s, %s);",
            (year, code, population),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    return {"detail": "Population record created."}


@router.put(
    "/{code}/population/{year}",
    status_code=status.HTTP_200_OK,
    tags=["Countries - Population"],
)
async def update_country_population(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    population: Annotated[int, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """PUT /countries/{code}/population/{year} — Update existing population data."""
    cur = get_cursor()
    cur.execute(
        "UPDATE population_per_year SET population = %s WHERE country_code = %s AND year = %s;",
        (population, code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No population record found for {code} in {year}")
    return {"detail": "Population record updated."}


@router.delete(
    "/{code}/population/{year}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Countries - Population"],
)
async def delete_country_population(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """DELETE /countries/{code}/population/{year} — Remove a population record."""
    cur = get_cursor()
    cur.execute(
        "DELETE FROM population_per_year WHERE country_code = %s AND year = %s;",
        (code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No population record found for {code} in {year}")
    return


@router.get(
    "/{code}/fishery",
    response_model=list[FisheryProductionPerYear],
    tags=["Countries - Fishery"],
)
async def get_country_fishery(
    code: str, user: Annotated[dict, Depends(get_current_user)]
):
    """GET /countries/{code}/fishery — Retrieve fishery production history for a country."""
    cur = get_cursor()
    cur.execute(
        "SELECT id, year, country_code, production FROM fishery_production_per_year "
        "WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        not_found(f"No fishery data for {code}")
    return [
        FisheryProductionPerYear(id=r[0], year=r[1], country_code=r[2], production=r[3])
        for r in rows
    ]


@router.post(
    "/{code}/fishery",
    status_code=status.HTTP_201_CREATED,
    tags=["Countries - Fishery"],
)
async def add_country_fishery(
    code: str,
    year: Annotated[int, Body(ge=0, le=9999)],
    production: Annotated[int, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """POST /countries/{code}/fishery — Add new fishery production data."""
    cur = get_cursor()
    try:
        cur.execute(
            "INSERT INTO fishery_production_per_year (year, country_code, production) VALUES (%s, %s, %s);",
            (year, code, production),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}") from e
    return {"detail": "Fishery record created."}


@router.put(
    "/{code}/fishery/{year}",
    status_code=status.HTTP_200_OK,
    tags=["Countries - Fishery"],
)
async def update_country_fishery(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    production: Annotated[int, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """PUT /countries/{code}/fishery/{year} — Update existing fishery production data."""
    cur = get_cursor()
    cur.execute(
        "UPDATE fishery_production_per_year SET production = %s WHERE country_code = %s AND year = %s;",
        (production, code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No fishery record found for {code} in {year}")
    return {"detail": "Fishery record updated."}


@router.delete(
    "/{code}/fishery/{year}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Countries - Fishery"],
)
async def delete_country_fishery(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """DELETE /countries/{code}/fishery/{year} — Remove a fishery record."""
    cur = get_cursor()
    cur.execute(
        "DELETE FROM fishery_production_per_year WHERE country_code = %s AND year = %s;",
        (code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No fishery record found for {code} in {year}")
    return


@router.get(
    "/{code}/seafood",
    response_model=list[SeafoodConsumptionPerCapitaPerYear],
    tags=["Countries - Seafood"],
)
async def get_country_seafood(
    code: str, user: Annotated[dict, Depends(get_current_user)]
):
    """GET /countries/{code}/seafood — Retrieve seafood consumption history for a country."""
    cur = get_cursor()
    cur.execute(
        "SELECT id, year, country_code, consumption FROM seafood_consumption_per_capita_per_year "
        "WHERE country_code = %s ORDER BY year;",
        (code,),
    )
    rows = cur.fetchall()
    if not rows:
        not_found(f"No seafood data for {code}")
    return [
        SeafoodConsumptionPerCapitaPerYear(
            id=r[0], year=r[1], country_code=r[2], consumption=r[3]
        )
        for r in rows
    ]


@router.post(
    "/{code}/seafood",
    status_code=status.HTTP_201_CREATED,
    tags=["Countries - Seafood"],
)
async def add_country_seafood(
    code: str,
    year: Annotated[int, Body(ge=0, le=9999)],
    consumption: Annotated[float, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """POST /countries/{code}/seafood — Add new seafood consumption data."""
    cur = get_cursor()
    try:
        cur.execute(
            "INSERT INTO seafood_consumption_per_capita_per_year (year, country_code, consumption) VALUES (%s, %s, %s);",
            (year, code, consumption),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    return {"detail": "Seafood record created."}


@router.put(
    "/{code}/seafood/{year}",
    status_code=status.HTTP_200_OK,
    tags=["Countries - Seafood"],
)
async def update_country_seafood(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    consumption: Annotated[float, Body(ge=0)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """PUT /countries/{code}/seafood/{year} — Update existing seafood consumption data."""
    cur = get_cursor()
    cur.execute(
        "UPDATE seafood_consumption_per_capita_per_year SET consumption = %s WHERE country_code = %s AND year = %s;",
        (consumption, code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No seafood record found for {code} in {year}")
    return {"detail": "Seafood record updated."}


@router.delete(
    "/{code}/seafood/{year}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Countries - Seafood"],
)
async def delete_country_seafood(
    code: str,
    year: Annotated[int, Path(ge=0, le=9999)],
    user: Annotated[dict, Depends(get_current_user)],
):
    """DELETE /countries/{code}/seafood/{year} — Remove a seafood record."""
    cur = get_cursor()
    cur.execute(
        "DELETE FROM seafood_consumption_per_capita_per_year WHERE country_code = %s AND year = %s;",
        (code, year),
    )
    if cur.rowcount == 0:
        not_found(f"No seafood record found for {code} in {year}")
    return
