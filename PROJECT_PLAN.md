# LabROI Project Plan

Automation Business Case Modeler for Laboratory Operations

Author: Morountudun (Arewa) Ojelade
Date: October 28, 2026
Status: M0 complete (October 28, 2026)

## 1. Vision

LabROI turns a lab workflow description plus an automation proposal into a reproducible, risk-adjusted business case: TCO (Total Cost of Ownership), NPV (Net Present Value), IRR (Internal Rate of Return), payback period, sensitivity analysis, and Monte Carlo risk, exported as a one-page report a leadership team can act on.

One command in, defensible answer out.

## 2. Why This Project

- Leadership conversations in laboratory operations and automation center on capital justification. Showing engineering ability is common; showing the finance layer is rare.
- Connects the MBA (Master of Business Administration) data science concentration to working software, the same way the engineering repos connect theory to code.
- Completes the family narrative with AirSOP and SterileView: run the bench, run the room, justify the purchase order.
- It is an engineering artifact, not a slide deck: versioned code, tested math, reproducible reports.

## 3. Problem

Lab automation business cases are usually built in personal spreadsheets:

- Point estimates only, no uncertainty: one savings number that collapses under a single finance question.
- No sensitivity view: nobody knows which assumption the decision actually hinges on.
- Validation burden forgotten: IQ/OQ/PQ (Installation Qualification, Operational Qualification, Performance Qualification), method transfer, and revalidation rarely appear as line items, so payback is understated.
- No version control: the model that justified last year's purchase cannot be re-run today.

Result: good projects stall in review, and weak projects get approved on optimistic math.

## 4. Core Concepts

| Term | Meaning | Where LabROI uses it |
|---|---|---|
| capex (capital expenditure) | One-time purchase cost | Year-0 cash flow |
| opex (operating expenditure) | Recurring annual cost | Baseline vs automated comparison |
| TCO (Total Cost of Ownership) | capex plus lifetime opex | Scenario comparison table |
| NPV (Net Present Value) | Discounted lifetime savings minus investment | Headline investment metric |
| IRR (Internal Rate of Return) | Discount rate where NPV equals zero | Finance-team shorthand |
| Payback period | Time until cumulative savings cover year-0 cost | Go/no-go threshold (many labs want under 24 months) |
| FTE (Full-Time Equivalent) | 2,080 labor hours per year | Hours-redeployed framing |
| TAT (Turnaround Time) | Sample-to-result time | Throughput benefit narrative |
| Monte Carlo | Sampling uncertain inputs many times | P(payback under 24 months), NPV distribution |

## 5. Architecture and Pipeline

Two JSON (JavaScript Object Notation) configs in, one business case out.

```
workflow.json + scenario.json
        |
        v
  validate (schema, units, ranges)
        |
        v
  engine.py     baseline annual cost vs automated annual cost
        |
        v
  finance.py    TCO, NPV, IRR, payback (simple + discounted)
        |
        v
  sensitivity.py (tornado chart) + montecarlo.py (risk)
        |
        v
  report.py     one-page markdown business case (+ charts)
        |
        v
  app.py        Streamlit dashboard (M4)
```

Every report is stamped with the config hash and code version, so any number can be regenerated exactly. Same audit instinct as the AirSOP hash-chained log.

## 6. Data Model

Workflow (the manual process today):

```json
{
  "name": "ELISA plate prep",
  "unit_name": "plate",
  "units_per_year": 5000,
  "hands_on_min_per_unit": 45,
  "loaded_labor_rate_per_hr": 52,
  "error_rate": 0.02,
  "rework_labor_hr": 0.75,
  "rework_material_cost": 85
}
```

Scenario (the automation proposal):

```json
{
  "name": "Liquid handler, 96-channel",
  "capex": 180000,
  "validation_cost": 35000,
  "training_cost": 5000,
  "service_pct_of_capex": 0.10,
  "consumables_delta_per_yr": 8000,
  "hands_on_min_per_unit": 8,
  "error_rate": 0.004,
  "implementation_delay_months": { "low": 3, "mode": 5, "high": 9 },
  "year1_utilization": { "low": 0.5, "mode": 0.7, "high": 0.9 },
  "horizon_years": 5,
  "discount_rate": 0.08
}
```

Uncertainty fields use triangular distributions (low, mode, high) so Monte Carlo has honest inputs instead of invented precision.

## 7. Golden Case (verified October 28, 2026)

Core lab running ELISA (Enzyme-Linked Immunosorbent Assay) plate prep, 20 plates/day, 250 days/year.

| Metric | Manual | Automated |
|---|---|---|
| Labor hours/year | 3,750 | 667 |
| Labor cost/year | $195,000.00 | $34,666.67 |
| Rework cost/year | $12,400.00 | $2,480.00 |
| Service + consumables/year | $0 | $26,000.00 |
| Total annual cost | $207,400.00 | $63,146.67 |

Year-0 investment: $220,000.00 ($180k instrument + $35k validation + $5k training)

| Result | Value |
|---|---|
| Annual savings | $144,253.33 |
| Simple payback | 1.53 years (18.3 months) |
| Discounted payback (8%) | 1.70 years (20.4 months) |
| NPV (8%, 5 years) | $355,961.73 |
| IRR | 59.15% |
| 5-year TCO | $1,037,000.00 vs $535,733.33 |
| Hours redeployed | 3,083/year (1.48 FTE) |

These values are the M0/M2 selfcheck golden numbers, asserted to the cent.

## 8. Milestones

### M0: Scaffold + finance core (one day)

- Public repo `labroi`, MIT license, README, requirements (numpy, matplotlib, pyyaml).
- `finance.py`: npv, irr (bisection with a no-solution guard), payback (simple and discounted), tco.
- `tests/selfcheck.py`: golden values asserted to the cent; edge cases (zero discount rate, savings at or below zero gives payback "never").
- Exit: suite green, output matches Section 7 exactly.

### M1: Workflow loader + baseline engine

- Config loaders with schema validation and human-readable error messages.
- Baseline annual cost from `workflow.json`; fixtures for two more workflows (sample accessioning, qPCR (quantitative Polymerase Chain Reaction) setup).
- Exit: baseline for all three fixtures matches hand math.

### M2: Scenario engine + business case report

- Apply a scenario to get automated annual cost, savings, and the cash-flow series.
- Three-way comparison: manual, semi-automated, fully automated.
- `report.py` generates a one-page markdown business case with config hash and version stamp.
- Exit: golden-case report regenerates byte-identical.

### M3: Uncertainty

- `sensitivity.py`: vary each assumption plus/minus 20%, render a tornado chart of NPV swing.
- `montecarlo.py`: triangular sampling on implementation delay, year-1 utilization, and error-rate improvement; outputs P(payback under 24 months) and an NPV fan chart.
- Exit: seeded runs reproduce exactly; charts render headless.

### M4: Dashboard

- `app.py` (Streamlit): a slider for every assumption, live NPV and payback, scenario table, report export.
- Exit: full workflow runs from the browser; dashboard numbers match the command line on identical config.

### M5: Polish + publish

- Second case study (sample accessioning with barcode automation).
- README with screenshots, LinkedIn post, 60-second screen-recorded walkthrough.
- Exit: a stranger can clone, run the selfcheck, and reproduce the golden case in under 5 minutes.

## 9. Testing Philosophy

Same flight-simulator rule as AirSOP and SterileView: no real instrument and no spreadsheet required to prove the math works. Golden numbers asserted to the cent, seeded randomness, and defined behavior for degenerate inputs (zero discount rate, negative savings, no-solution IRR).

## 10. Differentiators

1. Validation burden as a first-class line item: IQ/OQ/PQ, method transfer, revalidation. The cost every spreadsheet ROI estimate forgets in regulated labs.
2. Reproducible business cases: config hash plus version stamp on every report, so one command regenerates any number a CFO (Chief Financial Officer) questions.
3. Risk-adjusted output: P(payback under 24 months) instead of a single optimistic point estimate.
4. Decision honesty: the tornado chart shows which assumption the decision hinges on, so review meetings argue about the right number.
5. Labor framing: hours redeployed to higher-value testing, never headcount reduction. Written the way an operations leader actually presents it.

## 11. Scope Guardrails

Straight-line depreciation only (MACRS (Modified Accelerated Cost Recovery System) is a stretch goal), single site, US dollars, no tax-shield modeling in v1. Keep the engine small and exact rather than broad and approximate.

## 12. Portfolio Positioning

Money line for interviews: "AirSOP shows I can run the bench touchless, SterileView shows the same engine generalizes to the operating room, LabROI shows I can justify the purchase order."

Draft resume bullets:

- Built LabROI, a Python business-case engine for laboratory automation that computes TCO, NPV, IRR, and risk-adjusted payback from versioned workflow configs, with Monte Carlo sensitivity on implementation risk.
- Modeled a $220K liquid-handler justification (18.3-month payback, 59% IRR) including the IQ/OQ/PQ validation burden typically omitted from ROI estimates.

## 13. Build Slot

Fits after the AirSOP and SterileView build week. M0 to M2 in one focused day (the math core is compact), M3 to M5 across the following week.

## 14. Naming

Recommendation: **LabROI**, repo `labroi`. It says exactly what it does to a recruiter skimming a pinned repo list.

Alternates: CapexPilot, PaybackBench, AutoROI.
