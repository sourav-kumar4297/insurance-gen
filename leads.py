import json
from pathlib import Path

import pandas as pd

from config import DATA_XLSX, USED_PATH

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
}


def title_case_name(value):
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if not text:
        return ""
    return text.title()


def load_used():
    USED_PATH.parent.mkdir(parents=True, exist_ok=True)
    used = set(PREVIOUSLY_USED)
    if USED_PATH.exists():
        try:
            extra = json.loads(USED_PATH.read_text(encoding="utf-8"))
            used.update(str(item).strip().lower() for item in extra)
        except json.JSONDecodeError:
            pass
    return used


def save_used(used):
    USED_PATH.parent.mkdir(parents=True, exist_ok=True)
    USED_PATH.write_text(
        json.dumps(sorted(used), indent=2),
        encoding="utf-8",
    )


def remaining_count():
    return len(load_candidates())


def load_candidates():
    if not DATA_XLSX.exists():
        raise FileNotFoundError(
            f"Lead source not found: {DATA_XLSX}. Place the Excel file or set LEADS_XLSX."
        )

    df = pd.read_excel(DATA_XLSX)
    used = load_used()
    seen = set()
    candidates = []
    for _, record in df.iterrows():
        email = str(record.get("Email", "")).strip()
        if not email or email.lower() == "nan":
            continue
        key = email.lower()
        if key in used or key in seen:
            continue
        seen.add(key)
        candidates.append(
            {
                "first_name": title_case_name(record.get("FirstName")),
                "last_name": title_case_name(record.get("LastName")),
                "email": email,
            }
        )
    return candidates


def take_leads(count):
    candidates = load_candidates()
    if len(candidates) < count:
        raise ValueError(
            f"Need {count} unused contacts, found {len(candidates)} remaining."
        )
    selected = candidates[:count]
    used = load_used()
    used.update(person["email"].lower() for person in selected)
    save_used(used)
    return selected
