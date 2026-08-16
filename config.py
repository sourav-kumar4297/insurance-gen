import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Marissa2026!")

SITE_NAME = "Marissa Acosta NASB"
SITE_URL = "https://www.marissaacostanasb.com/"
FORM_NAME = "Google Ads Conversion - Button Click"
PDF_TITLE = "Google Ads Conversion — Button Click"

DEFAULT_LEAD_COUNT = 11
MIN_LEADS = 10
MAX_LEADS = 12
NEXT_EXPORT_NUMBER = 17

DATA_DIR = BASE_DIR / "data"
DATA_FILES = [
    DATA_DIR / "usa b2c consumers database-sample.xlsx",
    DATA_DIR / "usa traders-sample.xlsx",
    Path(r"c:\Users\DELL\Downloads\usa b2c consumers database-sample.xlsx"),
    Path(r"c:\Users\DELL\Downloads\usa traders-sample.xlsx"),
]
USED_PATH = BASE_DIR / "data" / "used.json"
STATE_PATH = BASE_DIR / "data" / "state.json"
GENERATED_DIR = BASE_DIR / "generated"
DOWNLOADS_DIR = Path(r"c:\Users\DELL\Downloads")

FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
