"""Mortgage interest rates for France (ECB MFI interest rate statistics).

Series MIR.M.FR.B.A2C.A.R.A.2250.EUR.N: bank interest rates on loans to
households for house purchase, new business, annualised agreed rate (AAR),
France, monthly, from 2000-01. Downloaded as CSV from the ECB Data Portal
(no key needed):

    https://data-api.ecb.europa.eu/service/data/MIR/M.FR.B.A2C.A.R.A.2250.EUR.N?format=csvdata

`load` returns the annual mean of the monthly rates, complete years only.
Used to turn house prices into a repayment burden (annuity over 25 years).
"""
import csv
import os
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

KEY = "M.FR.B.A2C.A.R.A.2250.EUR.N"
URL = f"https://data-api.ecb.europa.eu/service/data/MIR/{KEY}?format=csvdata"
FILE = "ecb_mir_house_purchase_fr.csv"


def fetch(raw_dir):
    out = Path(raw_dir) / "rates"
    out.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL, timeout=120) as resp:
        data = resp.read()
    if b"OBS_VALUE" not in data:
        raise RuntimeError("ECB MIR: unexpected response (no OBS_VALUE column)")
    part = out / (FILE + ".part")
    part.write_bytes(data)
    os.replace(part, out / FILE)
    print("wrote", out / FILE, f"({len(data):,} bytes)")


def load(raw_dir):
    path = Path(raw_dir) / "rates" / FILE
    months = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("OBS_VALUE"):
                year = int(row["TIME_PERIOD"][:4])
                months[year].append(float(row["OBS_VALUE"]) / 100)
    years = sorted(y for y, v in months.items() if len(v) == 12)
    return {
        "mortgage_rate": {
            "source": "ECB MFI interest rate statistics (MIR), France",
            "url": URL,
            "series_key": f"MIR.{KEY}",
            "unit": "annual rate (fraction), mean of 12 monthly values",
            "years": years,
            "values": [round(sum(months[y]) / 12, 5) for y in years],
            "notes": "Loans to households for house purchase, new business, annualised agreed rate. Complete years only.",
        }
    }


if __name__ == "__main__":
    fetch(sys.argv[1])
    r = load(sys.argv[1])["mortgage_rate"]
    print(f"{r['years'][0]}–{r['years'][-1]}: {r['values'][0]:.2%} … {r['values'][-1]:.2%}")
