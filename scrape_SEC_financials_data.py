# pull_sec_financials.py
import time
from pathlib import Path

import pandas as pd
import requests

# 1) Identify yourself to the SEC (required) so you don't get blocked.
USER_AGENT = "Anbu Nambi (anbunambi3108@gmail.com) - Student project"
HEADERS = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}

# 2) SEC base endpoints (stable, JSON)
BASE_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
BASE_FACTS       = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

FORM_OK = {"10-K", "10-K/A"}

# 3) Companies (CIKs must be 10-digit zero-padded strings)
COMPANIES = {
    "Microsoft": "0000789019",
    "Tesla":     "0001318605",
    "Apple":     "0000320193",
    "Amazon":    "0001018724",
    "Alphabet":  "0001652044",   # Google parent
    "Meta":      "0001326801",   # Facebook/Meta Platforms
    "Nvidia":    "0001045810",
    "Netflix":   "0001065280",
}

# 4) Which us-gaap tags correspond to the metrics we need (in priority order)
TAG_CHOICES = {
    "Total Revenue": [
        "Revenues", 
        "SalesRevenueNet", 
        "RevenueFromContractWithCustomerExcludingAssessedTax",
    ],
    "Net Income": [
        "NetIncomeLoss",
    ],
    "Total Assets": [
        "Assets",
    ],
    "Total Liabilities": [
        "Liabilities",
    ],
    "Operating Cash Flow": [
        "NetCashProvidedByUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    ],
}

# 5) Scale factors to convert reported units to plain USD (normalize your table)
UNIT_SCALE = {
    "USD": 1,
    "USDm": 1_000_000,
    "USDth": 1_000,   # occasionally seen
}

def get_json(url: str):
    """Small helper to GET JSON with proper headers and error handling."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def last_three_10k_fys(cik: str, verbose=True):
    data = get_json(BASE_SUBMISSIONS.format(cik=cik))
    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    fys   = filings.get("fy", [])
    years = []
    for form, fy in zip(forms, fys):
        if form in FORM_OK and fy and str(fy).isdigit():
            y = int(fy)
            if y not in years:
                years.append(y)
        if len(years) == 3:
            break
    if not years:
        if verbose:
            print(f"[WARN] No 10-K FYs via submissions for CIK {cik}. First 10 forms: {forms[:10]}")
        years = fallback_fys_from_facts(cik)
        if verbose:
            print(f"[INFO] Fallback years from facts: {years}")
    return years


def pick_units(units_dict: dict):
    """Choose the unit family and scale: prefer USD, then USDm, then anything available."""
    if not units_dict:
        return None, 1
    for pref in ("USD", "USDm", "USDth"):
        if pref in units_dict:
            return pref, UNIT_SCALE.get(pref, 1)
    # fallback to the first available key
    k = next(iter(units_dict.keys()))
    return k, UNIT_SCALE.get(k, 1)

def fact_value_for_fy(facts_json: dict, tag: str, fy_target: int):
    """
    Given companyfacts JSON, pull the value for a tag (e.g., 'Assets') for a specific fiscal year.
    Prefer entries from 10-K and full-year periods (fp='FY' or 'YTD').
    """
    facts = facts_json.get("facts", {}).get("us-gaap", {})
    if tag not in facts:
        return None
    unit_key, scale = pick_units(facts[tag].get("units"))
    if unit_key is None:
        return None
    for row in facts[tag]["units"][unit_key]:
        if row.get("fy") == fy_target and row.get("form") in FORM_OK and row.get("fp") in (None, "FY", "YTD"):
            val = row.get("val")
            return float(val) * scale if val is not None else None
    return None

def pull_company(company: str, cik: str):
    """Fetch the last three FYs and all required metrics for one company."""
    fys = last_three_10k_fys(cik)
    time.sleep(0.2)  # polite pause
    facts = get_json(BASE_FACTS.format(cik=cik))
    rows = []
    for fy in fys:
        metrics = {}
        for nice_name, tags in TAG_CHOICES.items():
            v = None
            for tag in tags:
                v = fact_value_for_fy(facts, tag, fy)
                if v is not None:
                    break
            metrics[nice_name] = v
        rows.append({
            "Company": company,
            "Fiscal Year": fy,
            "Total Revenue": metrics["Total Revenue"],
            "Net Income": metrics["Net Income"],
            "Total Assets": metrics["Total Assets"],
            "Total Liabilities": metrics["Total Liabilities"],
            "Operating Cash Flow": metrics["Operating Cash Flow"],
        })
    return rows
def fallback_fys_from_facts(cik: str):
    """
    If the submissions feed didn't yield FYs, infer them from the facts file
    by scanning a ubiquitous tag (Assets) and collecting years reported on 10-K/10-K/A.
    """
    facts = get_json(BASE_FACTS.format(cik=cik))
    us = facts.get("facts", {}).get("us-gaap", {})
    years = set()
    units = us.get("Assets", {}).get("units", {})  # Assets exists basically every year
    for arr in units.values():
        for row in arr:
            fy = row.get("fy")
            form = row.get("form")
            if isinstance(fy, int) and form in FORM_OK:
                years.add(fy)
    return sorted(years, reverse=True)[:3]

def main():
    all_rows = []
    for name, cik in COMPANIES.items():
        all_rows.extend(pull_company(name, cik))
        time.sleep(0.3)
    df = pd.DataFrame(all_rows).sort_values(["Company", "Fiscal Year"])
    # Compute YoY growth (%) by company for each metric
    for col in ["Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Operating Cash Flow"]:
        df[f"{col} YoY (%)"] = (df.groupby("Company")[col].pct_change() * 100).round(2)
    out_dir = Path("sec_outputs"); out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / "financials.csv", index=False)
    df.to_excel(out_dir / "financials.xlsx", index=False)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
