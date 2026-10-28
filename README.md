# LabROI

Automation business case modeler for laboratory operations.

Two JSON configs in, one defensible business case out: total cost of ownership, net present value, internal rate of return, simple and discounted payback, sensitivity analysis, and Monte Carlo risk, exported as a one-page report stamped with a config hash and code version so every number can be regenerated exactly.

## Why

Lab automation business cases usually live in fragile spreadsheets: point estimates only, no sensitivity view, validation costs (IQ/OQ/PQ, method transfer) forgotten, no version control. Good projects stall in finance review and weak projects get approved on optimistic math. LabROI makes the business case a tested, versioned artifact.

## Golden case

ELISA plate prep, 20 plates/day, 250 days/year. Year-0 investment $220,000 (instrument + validation + training).

| Result | Value |
|---|---|
| Annual savings | $144,253.33 |
| Simple payback | 18.3 months |
| Discounted payback (8%) | 20.4 months |
| NPV (8%, 5 years) | $355,961.73 |
| IRR | 59.15% |
| 5-year TCO | $1,037,000.00 manual vs $535,733.33 automated |
| Hours redeployed | 3,083/year (1.48 FTE) |

Every number above is asserted to the cent by the selfcheck.

## Quickstart

```
pip install -r requirements.txt
python tests/selfcheck.py
```

## Roadmap

- [x] M0: finance core (npv, irr, payback simple + discounted, tco) and golden-case selfcheck
- [ ] M1: workflow loader and baseline cost engine
- [ ] M2: scenario engine and one-page markdown business case
- [ ] M3: tornado sensitivity and Monte Carlo risk
- [ ] M4: Streamlit dashboard
- [ ] M5: polish and publish

## Testing philosophy

Flight-simulator rule: no instrument and no spreadsheet required to prove the math works. Golden numbers asserted to the cent, seeded randomness, and defined behavior for degenerate inputs (zero discount rate, negative savings, no-solution IRR).

## License

MIT
