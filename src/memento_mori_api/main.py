"""memento_mori_api.main

FastAPI application providing life statistics.

This module exposes a single endpoint, POST /life-stats, that accepts a
birthday and life expectancy and returns the number of weeks left and the
percentage of life already lived. All times are treated in UTC.

Examples
--------
Request JSON
>>> {
...   "birthday": "1990-01-01",
...   "life_expectancy": 80
... }

Response JSON
>>> {
...   "weeks_left": 3200,
...   "percentage_lived": 40.12
... }
"""

import logging
from datetime import date, datetime

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .timezone import TZ

logger = logging.getLogger(__name__)

app = FastAPI()


class LifeStatsRequest(BaseModel):
    """Request model for life statistics.

    Attributes
    ----------
    birthday : date
        Birthday in YYYY-MM-DD format.
    life_expectancy : float
        Life expectancy in years.
    """

    birthday: date = Field(..., description="Birthday in YYYY-MM-DD format")
    life_expectancy: float = Field(..., description="Life expectancy in years")


class LifeStatsResponse(BaseModel):
    """Response model for life statistics.

    Attributes
    ----------
    weeks_left : int
        Estimated number of weeks remaining (rounded down).
    percentage_lived : float
        Percentage of life already lived (0-100), rounded to 2 decimals.
    """

    weeks_left: int
    percentage_lived: float


@app.post("/life-stats", response_model=LifeStatsResponse)
def life_stats(data: LifeStatsRequest) -> LifeStatsResponse:
    """Compute simple life statistics for a person.

    Parameters
    ----------
    data : LifeStatsRequest
        Request payload containing the person's birthday and life expectancy
        (in years).

    Returns
    -------
    LifeStatsResponse
        Response model containing:
        - ``weeks_left``: number of weeks remaining until the expected end of life
          (non-negative integer).
        - ``percentage_lived``: percentage of life already lived, clamped to 100.0
          and rounded to two decimal places.

    Notes
    -----
    - The calculation uses 365.25 days per year to roughly account for leap years.
    - Life expectancy in years is converted to weeks using 52.1775 weeks/year.
    - ``weeks_left`` is computed using integer weeks lived (truncation) and will
      never be negative.

    Examples
    --------
    >>> payload = LifeStatsRequest(birthday=date(1990, 1, 1), life_expectancy=80)
    >>> life_stats(payload)
    LifeStatsResponse(weeks_left=..., percentage_lived=...)
    """

    today = datetime.now(tz=TZ).date()
    age_days = (today - data.birthday).days
    age_years = age_days / 365.25
    total_weeks = int(data.life_expectancy * 52.1775)
    lived_weeks = int(age_days / 7)
    weeks_left = max(total_weeks - lived_weeks, 0)
    percentage_lived = min((age_years / data.life_expectancy) * 100, 100.0)
    return LifeStatsResponse(
        weeks_left=weeks_left, percentage_lived=round(percentage_lived, 2)
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
