from datetime import date, datetime, timedelta
from functools import wraps

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
    GENERATED_DIR,
    MAX_LEADS,
    MIN_LEADS,
    SECRET_KEY,
    SITE_NAME,
    SITE_URL,
)
from lead_pdf import build_pdf, format_generated_on, random_submission_times
from leads import remaining_count, take_leads

app = Flask(__name__)
app.secret_key = SECRET_KEY

LAST_EXPORT_END = date(2026, 8, 12)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


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
    try:
        leftover = remaining_count()
        source_ok = True
        source_error = ""
    except Exception as exc:
        leftover = 0
        source_ok = False
        source_error = str(exc)

    return render_template(
        "dashboard.html",
        site_name=SITE_NAME,
        site_url=SITE_URL,
        remaining=leftover,
        source_ok=source_ok,
        source_error=source_error,
        min_leads=MIN_LEADS,
        max_leads=MAX_LEADS,
        default_count=DEFAULT_LEAD_COUNT,
        start_date=(LAST_EXPORT_END + timedelta(days=1)).isoformat(),
        today=date.today().isoformat(),
    )


@app.route("/generate", methods=["POST"])
@login_required
def generate():
    try:
        count = int(request.form.get("count") or DEFAULT_LEAD_COUNT)
    except ValueError:
        count = DEFAULT_LEAD_COUNT
    count = max(MIN_LEADS, min(MAX_LEADS, count))

    start = date.fromisoformat(
        request.form.get("start_date") or str(LAST_EXPORT_END + timedelta(days=1))
    )
    end = date.fromisoformat(request.form.get("end_date") or str(date.today()))
    if start > end:
        start, end = end, start

    try:
        selected = take_leads(count)
        timestamps = random_submission_times(count, start, end)
        rows = []
        for index, (person, submitted_on) in enumerate(zip(selected, timestamps), start=1):
            rows.append({**person, "submitted_on": submitted_on, "index": index})

        generated_on = format_generated_on(date.today())
        filename = f"Website Visit - Consultation Request - Export ({datetime.now().strftime('%Y%m%d-%H%M%S')}).pdf"
        output_path = GENERATED_DIR / filename
        build_pdf(rows, output_path, start, end, generated_on)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception as exc:
        flash(str(exc))
        return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    app.run(debug=True, port=5050)
