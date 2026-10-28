"""Core finance math for LabROI.

All functions are pure and deterministic. Money is float dollars; callers
round to cents at presentation time.
"""

from __future__ import annotations

import math
from typing import Optional, Sequence

FTE_HOURS_PER_YEAR = 2080.0


def npv(rate: float, cashflows: Sequence[float]) -> float:
    """Net present value. cashflows[0] occurs at t=0."""
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def annuity_factor(rate: float, years: int) -> float:
    """Present value of 1.0 received at the end of each year."""
    if years < 0:
        raise ValueError("years must be >= 0")
    if rate == 0.0:
        return float(years)
    return (1.0 - (1.0 + rate) ** -years) / rate


def irr(
    cashflows: Sequence[float],
    lo: float = -0.9999,
    hi: float = 10.0,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> Optional[float]:
    """Internal rate of return by bisection.

    Returns None when no sign change brackets a root in (lo, hi), i.e. the
    cash-flow series has no solution (for example, all-positive flows).
    """
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return 0.5 * (lo + hi)


def payback_simple(year0: float, annual_savings: float) -> float:
    """Years until undiscounted savings cover the year-0 cost.

    Returns math.inf when savings never cover the investment.
    """
    if annual_savings <= 0.0:
        return math.inf
    return year0 / annual_savings


def payback_discounted(
    rate: float, year0: float, annual_savings: float, horizon_years: int
) -> float:
    """Years until discounted savings cover the year-0 cost.

    Interpolates linearly within the recovery year. Returns math.inf when
    the investment is not recovered within horizon_years.
    """
    cumulative = 0.0
    for t in range(1, horizon_years + 1):
        cf = annual_savings / (1.0 + rate) ** t
        if cumulative + cf >= year0:
            return (t - 1) + (year0 - cumulative) / cf
        cumulative += cf
    return math.inf


def tco(year0: float, annual_cost: float, years: int) -> float:
    """Total cost of ownership over a horizon."""
    return year0 + annual_cost * years


def format_payback(years: float) -> str:
    """Human-readable payback, e.g. '1.53 yr (18.3 mo)' or 'never'."""
    if math.isinf(years):
        return "never"
    return f"{years:.2f} yr ({years * 12:.1f} mo)"
