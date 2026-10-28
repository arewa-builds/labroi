"""LabROI M0 selfcheck: golden-case finance math, asserted to the cent.

Golden values come from PROJECT_PLAN.md Section 7 (verified 2026-10-28).

Run: python tests/selfcheck.py
"""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.finance import (  # noqa: E402
    FTE_HOURS_PER_YEAR,
    annuity_factor,
    irr,
    npv,
    payback_discounted,
    payback_simple,
    tco,
)

# --- Golden case primitives (PROJECT_PLAN.md Section 7) ---------------------
PLATES = 5000                     # 20 plates/day x 250 days
MIN_MANUAL, MIN_AUTO = 45.0, 8.0  # hands-on minutes per plate
RATE = 52.0                       # loaded labor dollars per hour
ERR_MANUAL, ERR_AUTO = 0.02, 0.004
REWORK = 0.75 * RATE + 85.0       # labor + reagents per failed plate
CAPEX, VALIDATION, TRAINING = 180000.0, 35000.0, 5000.0
SERVICE = 0.10 * CAPEX            # annual service contract
CONSUMABLES = 8000.0              # annual consumables delta
HORIZON, DISCOUNT = 5, 0.08


def golden_case():
    h_manual = PLATES * MIN_MANUAL / 60.0
    h_auto = PLATES * MIN_AUTO / 60.0
    baseline = h_manual * RATE + PLATES * ERR_MANUAL * REWORK
    automated = (
        h_auto * RATE + PLATES * ERR_AUTO * REWORK + SERVICE + CONSUMABLES
    )
    year0 = CAPEX + VALIDATION + TRAINING
    savings = baseline - automated
    return h_manual, h_auto, baseline, automated, year0, savings


def main() -> int:
    h_manual, h_auto, baseline, automated, year0, savings = golden_case()
    cashflows = [-year0] + [savings] * HORIZON
    r = irr(cashflows)

    checks = []

    def check(name, ok):
        checks.append((name, bool(ok)))

    check("golden baseline annual cost", round(baseline, 2) == 207400.00)
    check("golden automated annual cost", round(automated, 2) == 63146.67)
    check("golden annual savings", round(savings, 2) == 144253.33)
    check("golden npv (8%, 5 yr)", round(npv(DISCOUNT, cashflows), 2) == 355961.73)
    check("golden irr", r is not None and round(r * 100, 2) == 59.15)
    check(
        "simple payback 18.3 months",
        round(payback_simple(year0, savings) * 12, 1) == 18.3,
    )
    check(
        "discounted payback 20.4 months",
        round(payback_discounted(DISCOUNT, year0, savings, HORIZON) * 12, 1) == 20.4,
    )
    check("tco manual 5 yr", round(tco(0.0, baseline, HORIZON), 2) == 1037000.00)
    check(
        "tco automated 5 yr", round(tco(year0, automated, HORIZON), 2) == 535733.33
    )
    check(
        "fte redeployed",
        round((h_manual - h_auto) / FTE_HOURS_PER_YEAR, 2) == 1.48,
    )
    check(
        "zero discount rate",
        npv(0.0, [-100.0, 60.0, 60.0]) == 20.0
        and annuity_factor(0.0, 5) == 5.0
        and round(payback_discounted(0.0, 100.0, 60.0, 5), 6) == round(5.0 / 3.0, 6),
    )
    check(
        "payback never (savings <= 0 or beyond horizon)",
        math.isinf(payback_simple(1000.0, -5.0))
        and math.isinf(payback_discounted(0.08, 1000.0, -5.0, 5))
        and math.isinf(payback_discounted(0.5, 1000.0, 100.0, 5)),
    )
    check("irr no solution returns None", irr([100.0, 100.0, 100.0]) is None)

    failed = 0
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        failed += 0 if ok else 1
    total = len(checks)
    print(f"\n{total - failed}/{total} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
