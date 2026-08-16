# insurance-gen

Login page for generating Squarespace-style Google Ads conversion PDFs — same format as the earlier exports (11)–(16).

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5050

Default login:

- username: `admin`
- password: `Marissa2026!`

Change these with `ADMIN_USER`, `ADMIN_PASSWORD`, and `SECRET_KEY`.

## Lead source

The generator reads unused contacts from:

- `c:\Users\DELL\Downloads\usa b2c consumers database-sample.xlsx`
- `c:\Users\DELL\Downloads\usa traders-sample.xlsx`

Emails already used in exports (11)–(16) are skipped. Each Generate click marks the new emails as used so they are never repeated.

## Dates

Pick a start and end date on the dashboard. The PDF header **Date range** and every **SUBMITTED ON** timestamp use that range:

- first row falls on the start date
- last row falls on the end date
- remaining rows are spread across the days in between
- Generated date is the end date (same as previous exports)

Default start date is the day after the last generated export.

## Output

Click **Generate leads** to download a landscape PDF named:

`Google Ads Conversion - Button Click - Squarespace Export (N).pdf`

A copy is also saved to Downloads. Layout matches the earlier files:

- columns: `# | FORM NAME | SUBMITTED ON | FIRST NAME | LAST NAME | EMAIL`
- form name: `Google Ads Conversion - Button Click`
- 10–12 unique names/emails
