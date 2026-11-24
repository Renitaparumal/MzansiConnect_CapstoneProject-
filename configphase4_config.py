config/phase4_config.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

FILE_PATHS = {
    "customers": RAW_DATA_DIR / "customers.csv",
    "usage": RAW_DATA_DIR / "usage.csv",
    "tickets": RAW_DATA_DIR / "tickets.csv",
    "data_dictionary": RAW_DATA_DIR / "data_dictionary.csv",
}

PLACEHOLDER_VALUES = [-999, "-999", "", "NA", "N/A", "null", "None"]

PROVINCE_MAP = {
    "gp": "Gauteng",
    "gauteng": "Gauteng",
    "wc": "Western Cape",
    "western cape": "Western Cape",
    "kzn": "KwaZulu-Natal",
    "kwazulu-natal": "KwaZulu-Natal",
    "kwazulu natal": "KwaZulu-Natal",
    "ec": "Eastern Cape",
    "eastern cape": "Eastern Cape",
    "fs": "Free State",
    "free state": "Free State",
    "lp": "Limpopo",
    "limpopo": "Limpopo",
    "mp": "Mpumalanga",
    "mpumalanga": "Mpumalanga",
    "nc": "Northern Cape",
    "northern cape": "Northern Cape",
    "nw": "North West",
    "north west": "North West",
}

PLAN_TYPE_MAP = {
    "prepaid": "Prepaid",
    "pre-paid": "Prepaid",
    "postpaid": "Postpaid",
    "post-paid": "Postpaid",
    "hybrid": "Hybrid",
}

BINARY_MAP = {
    "yes": 1,
    "y": 1,
    "true": 1,
    "1": 1,
    "no": 0,
    "n": 0,
    "false": 0,
    "0": 0,
}

VALIDATION_BOUNDS = {
    "age_min": 18,
    "age_max": 100,
    "max_date": "2026-07-31",
}
