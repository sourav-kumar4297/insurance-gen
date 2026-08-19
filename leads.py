import json
from pathlib import Path

import pandas as pd

from config import CONTACTS_PATH, DATA_FILES, STATE_PATH, USED_PATH

PREVIOUSLY_USED = {
    "bryanburgen1@hotmail.com",
    "monuskos@aol.com",
    "stephanieguyer@gmail.com",
    "anesseth@gmail.com",
    "nrizzo@hotmail.com",
    "blythesolace@comcast.net",
    "johnh@erols.com",
    "cherylkula@hotmail.com",
    "catera4lcd@comcast.net",
    "gurgies@msn.com",
    "nfsolutions@hotmail.com",
    "sszendre@yahoo.com",
    "donle2@msn.com",
    "mark.oursland@gmail.com",
    "martinez-3@msn.com",
    "lek_allen@hotmail.com",
    "praise0224@hotmail.com",
    "justine.brewer@att.net",
    "pcon38@yahoo.com",
    "electrichead00@hotmail.com",
    "pinkpixiejess@yahoo.com",
    "wondar1204@aol.com",
    "tyreejackson@hotmail.com",
    "myman7866@comcast.net",
    "davidaleger@yahoo.com",
    "adurina7@hotmail.com",
    "trinidad978@yahoo.com",
    "almax48@hotmail.com",
    "acalapristi@aol.com",
    "starbuck_21@hotmail.com",
    "dann@insightbb.com",
    "travis_17@msn.com",
    "snbenzel@msn.com",
    "rodney_a_anderson@yahoo.com",
    "annadavis01@hotmail.com",
    "pj1patterson@aol.com",
    "brandon6464@live.com",
    "ritatiwari@gmail.com",
    "comeback.king@hotmail.com",
    "yohead70@yahoo.com",
    "eahoyt@aol.com",
    "prdomm@aol.com",
    "lbarbash@hotmail.com",
    "alice.love39@gmail.com",
    "leonletwin@aol.com",
    "gam9r@yahoo.com",
    "chikenguy13@yahoo.com",
    "betttaps@aol.com",
    "brianbyles@aol.com",
    "myavalar@aol.com",
    "gary_125@hotmail.com",
    "isisp@yahoo.com",
    "ms.chiquitalee@yahoo.com",
    "nalten@hotmail.com",
    "rentmoneyjob@yahoo.com",
    "dulceyarihanny08@yahoo.com",
    "billionaireslife@aol.com",
    "taestbang@gmail.com",
    "grandg7@hotmail.com",
    "michelleb160@hotmail.com",
    "ari.roth@gmail.com",
    "allencaldwell008@gmail.com",
    "chand31@msn.com",
    "aeyassu@aol.com",
    "visionwrx2@yahoo.com",
    "mybermuda@aol.com",
    "dallibeth_estevez@hotmail.com",
    # Older reference export emails — never reuse
    "mark.bagley@bt.com",
    "espositosal@italianwinemerchants.com",
    "marc@mgc.solutions",
    "alan.pace@citigroup.com",
    "apetroni@gmail.com",
    "borowiczj@dteenergy.com",
    "ahmed@automatework.com",
    "walt.czerminski@bbh.com",
    "yang_276@yahoo.com",
    "db.forsberg@gmail.com",
    "dladouceur@22citylink.com",
    "rredmer@choctawnation.com",
    "jason@benzinga.com",
    "eric_kovalak@hotmail.com",
    "brant.arseneau@bmo.com",
    "nazia@u.northwestern.edu",
    "suzyley77@gmail.com",
    "farah@lyft.com",
    "ak@intellicagroup.com",
    "mushgie@gmail.com",
    "rorman@mortgagefulfillment.com",
    "ta@thehorizongroup.com",
    "george.langas@svn.com",
    "harriphil@gmail.com",
    "andrew@inhinge.com",
    "mjlevas@olympiancapital.com",
    "kiato4@gmail.com",
    "chen.kristin@gmail.com",
    "sandra.myburgh@gmail.com",
    "rodrigoocejo@avalancha.ventures",
    "richard-reynolds@uiowa.edu",
    "nancy.stern@kattenlaw.com",
    "michaelwebsterii@hotmail.com",
    "tpettipiece@tradevela.com",
    "erik.chase.johnson@gmail.com",
    "estonwoodard@gmail.com",
    "silvia@equities.com",
    "daniel@aerserv.com",
    "alawrence@leapmotion.com",
    "ryan@outpostvc.com",
    "pshiner@performancetrust.com",
    "johnkmikhael@gmail.com",
    "hulsha@pepperlaw.com",
    "pvshrijal@gmail.com",
    "dbielik@tcgservices.com",
}


def title_case_name(value):
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return ""
    return text.title()


def record_value(record, *keys):
    lookup = {}
    for column in record.index:
        lookup[str(column).strip().lower().replace(" ", "").replace("_", "")] = column
    for key in keys:
        mapped = lookup.get(str(key).strip().lower().replace(" ", "").replace("_", ""))
        if mapped is not None:
            return record.get(mapped)
    return None


def row_from_record(record):
    email = str(record_value(record, "Email", "E-mail") or "").strip()
    if not email or email.lower() == "nan":
        return None
    first = title_case_name(record_value(record, "FirstName", "First Name", "first_name"))
    last = title_case_name(record_value(record, "LastName", "Last Name", "last_name"))
    if not first and not last:
        contact = title_case_name(record_value(record, "Contact Name", "ContactName", "Name"))
        parts = contact.split(None, 1)
        first = parts[0] if parts else ""
        last = parts[1] if len(parts) > 1 else ""
    return {"first_name": first, "last_name": last, "email": email}


def load_used():
    used = set(PREVIOUSLY_USED)
    try:
        USED_PATH.parent.mkdir(parents=True, exist_ok=True)
        if USED_PATH.exists():
            extra = json.loads(USED_PATH.read_text(encoding="utf-8"))
            if isinstance(extra, list):
                used.update(str(item).strip().lower() for item in extra)
    except Exception:
        pass
    return used


def save_used(used):
    try:
        USED_PATH.parent.mkdir(parents=True, exist_ok=True)
        USED_PATH.write_text(
            json.dumps(sorted(used), indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def remaining_count():
    return len(load_candidates())


def load_state():
    default = {"export_number": 17, "last_end_date": "2026-08-12"}
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if STATE_PATH.exists():
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                default.update(data)
    except Exception:
        pass
    return default


def save_state(state):
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


def _from_json():
    paths = [
        CONTACTS_PATH,
        Path(__file__).resolve().parent / "data" / "contacts.json",
        Path.cwd() / "data" / "contacts.json",
    ]
    seen = set()
    for path in paths:
        try:
            resolved = path.resolve()
        except Exception:
            resolved = path
        key = str(resolved).lower()
        if key in seen or not path.exists():
            continue
        seen.add(key)
        try:
            raw = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if not isinstance(raw, list):
            continue
        rows = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            email = str(item.get("email") or "").strip()
            if not email:
                continue
            rows.append(
                {
                    "first_name": str(item.get("first_name") or "").strip(),
                    "last_name": str(item.get("last_name") or "").strip(),
                    "email": email,
                }
            )
        if rows:
            return rows
    return []


def _from_excel():
    existing = []
    seen_paths = set()
    for path in DATA_FILES:
        try:
            if not path.exists():
                continue
            key = str(path.resolve()).lower()
        except Exception:
            continue
        if key in seen_paths:
            continue
        seen_paths.add(key)
        existing.append(path)

    rows = []
    for path in existing:
        try:
            df = pd.read_excel(path)
        except Exception:
            continue
        for _, record in df.iterrows():
            person = row_from_record(record)
            if person:
                rows.append(person)
    return rows


def load_candidates():
    used = load_used()
    seen = set()
    candidates = []
    source_rows = []
    try:
        source_rows.extend(_from_excel())
    except Exception:
        pass
    try:
        source_rows.extend(_from_json())
    except Exception:
        pass
    for person in source_rows:
        key = person["email"].lower()
        if key in used or key in seen:
            continue
        seen.add(key)
        candidates.append(person)
    return candidates


def peek_leads(count):
    candidates = load_candidates()
    if not candidates:
        raise ValueError("NO_VISITORS")
    return candidates[: max(1, count)]


def mark_used(people):
    used = load_used()
    used.update(person["email"].lower() for person in people)
    save_used(used)
