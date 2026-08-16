# insurance-gen

Login page for generating unique website-visit lead PDFs for [marissaacostanasb.com](https://www.marissaacostanasb.com/).

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

The generator reads:

`c:\Users\DELL\Downloads\usa b2c consumers database-sample.xlsx`

Override with `LEADS_XLSX`. Previously used emails are skipped, and each Generate Leads click marks the new emails as used so they are not repeated.

## Output

Click **Generate leads** to download a landscape PDF in the same Squarespace export layout:

- 10–12 unique names/emails
- dates from the last export through today
- form name: Website Visit — Consultation Request
