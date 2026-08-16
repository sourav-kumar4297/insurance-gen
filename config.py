import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Marissa2026!")

SITE_NAME = "Marissa Acosta NASB"
SITE_URL = "https://www.marissaacostanasb.com/"
FORM_NAME = "Website Visit — Consultation Request"

DEFAULT_LEAD_COUNT = 11
MIN_LEADS = 10
MAX_LEADS = 12

DATA_XLSX = Path(
    os.environ.get(
        "LEADS_XLSX",
        r"c:\Users\DELL\Downloads\usa b2c consumers database-sample.xlsx",
    )
)
USED_PATH = BASE_DIR / "data" / "used.json"
GENERATED_DIR = BASE_DIR / "generated"

FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
