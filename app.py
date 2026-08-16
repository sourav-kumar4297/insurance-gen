from datetime import date, timedelta
from functools import wraps
from shutil import copy2

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from config import (
    ADMIN_PASSWORD,
    ADMIN_USER,
    DEFAULT_LEAD_COUNT,
    DOWNLOADS_DIR,
    GENERATED_DIR,
    MAX_LEADS,
    MIN_LEADS,
    SECRET_KEY,
    SITE_NAME,
)
from lead_pdf import build_pdf, format_generated_on, random_submission_times
from leads import load_state, mark_used, peek_leads, remaining_count, save_state

app = Flask(__name__)
app.secret_key = SECRET_KEY


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def parse_date(value, fallback):
    try:
        return date.fromisoformat((value or "").strip())
    except ValueError:
        return fallback


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.")

    return render_template("login.html", site_name=SITE_NAME)


@app.route("/dashboard")
@login_required
def dashboard():
    state = load_state()
    last_end = parse_date(state.get("last_end_date"), date(2026, 8, 12))
    default_start = last_end + timedelta(days=1)
    default_end = date.today()
    if default_start > default_end:
        default_start = default_end

    try:
        leftover = remaining_count()
        source_ok = leftover >= MIN_LEADS
    except Exception:
        leftover = 0
        source_ok = False

    return render_template(
        "dashboard.html",
        site_name=SITE_NAME,
        source_ok=source_ok,
        default_count=DEFAULT_LEAD_COUNT,
        start_date=default_start.isoformat(),
        today=default_end.isoformat(),
    )


@app.route("/generate", methods=["POST"])
@login_required
def generate():
    state = load_state()
    last_end = parse_date(state.get("last_end_date"), date(2026, 8, 12))
    default_start = last_end + timedelta(days=1)
    default_end = date.today()

    try:
        count = int(request.form.get("count") or DEFAULT_LEAD_COUNT)
    except ValueError:
        count = DEFAULT_LEAD_COUNT
    count = max(MIN_LEADS, min(MAX_LEADS, count))

    start = parse_date(request.form.get("start_date"), default_start)
    end = parse_date(request.form.get("end_date"), default_end)
    if start > end:
        start, end = end, start

    try:
        selected = peek_leads(count)
        timestamps = random_submission_times(count, start, end)
        covered = {item.date() for item in timestamps}
        if start not in covered or end not in covered:
            raise ValueError("Please choose a valid date range.")

        rows = []
        for index, (person, submitted_on) in enumerate(zip(selected, timestamps), start=1):
            rows.append({**person, "submitted_on": submitted_on, "index": index})

        generated_on = format_generated_on(end)
        export_number = int(state.get("export_number") or 17)
        filename = f"Google Ads Conversion - Button Click - Squarespace Export ({export_number}).pdf"
        output_path = GENERATED_DIR / filename
        build_pdf(rows, output_path, start, end, generated_on)

        DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
        copy2(output_path, DOWNLOADS_DIR / filename)

        mark_used(selected)
        state["export_number"] = export_number + 1
        state["last_end_date"] = end.isoformat()
        save_state(state)

        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception:
        flash("Unable to generate export right now. Please try again.")
        return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    app.run(debug=True, port=5050)
