from flask import Flask, redirect, render_template, request, url_for, jsonify
from dotenv import load_dotenv
import os
import git
import hmac
import hashlib
from db import db_read, db_write
from auth import login_manager, authenticate, register_user
from flask_login import login_user, logout_user, login_required, current_user
import logging
from categories import CATEGORIES, BARCODES

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Load .env variables
load_dotenv()
W_SECRET = os.getenv("W_SECRET")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "supersecret-dev-only")

# Init flask app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = APP_SECRET_KEY

# Init auth
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================
# PUNKTE-SYSTEM
# =========================
POINTS_PER_WASTE = {
    "pet": 5,
    "glas": 3,
    "aluminium": 2,
    "papier": 1
}


def get_user_points(user_id):
    """Hole Punkte fuer einen Benutzer aus der DB"""
    result = db_read(
        "SELECT points FROM user_points WHERE user_id=%s",
        (user_id,),
        single=True
    )
    if result is None:
        return 0
    return result.get("points", 0)


def add_user_points(user_id, amount):
    """Addiere Punkte zu einem Benutzer"""
    from db import db_upsert
    current = get_user_points(user_id)
    new_points = current + amount
    db_upsert(user_id, new_points)


# =========================
# WEBHOOK (robust)
# =========================
@app.route("/update_server", methods=["POST"])
def webhook():
    """
    GitHub Webhook Endpoint.
    Akzeptiert sha256 (X-Hub-Signature-256) und sha1 (X-Hub-Signature).
    Gibt 401 zurueck wenn Secret/Signatur fehlt oder nicht passt.
    """
    sig256 = request.headers.get("X-Hub-Signature-256")
    sig1 = request.headers.get("X-Hub-Signature")
    signature = sig256 or sig1

    if not signature or not W_SECRET:
        logging.warning("Webhook: Missing signature header or W_SECRET not set")
        return "Unauthorized", 401

    try:
        hash_algorithm, github_signature = signature.split("=", 1)
        algorithm = hashlib.__dict__.get(hash_algorithm)

        if algorithm is None:
            logging.warning("Webhook: Unsupported hash algorithm: %s", hash_algorithm)
            return "Unauthorized", 401

        mac = hmac.new(
            W_SECRET.encode("utf-8"),
            msg=request.data,
            digestmod=algorithm
        )

        if not hmac.compare_digest(mac.hexdigest(), github_signature):
            logging.warning("Webhook: Signature mismatch")
            return "Unauthorized", 401

    except Exception as e:
        logging.warning("Webhook: Signature parse/verify failed: %s", e)
        return "Unauthorized", 401

    # Pull Repo
    try:
        repo = git.Repo("./mysite")
        origin = repo.remotes.origin
        origin.pull()
        logging.info("Webhook: Pulled successfully")
        return "Updated successfully", 200
    except Exception as e:
        logging.warning("Webhook pull failed: %s", e)
        return "Pull failed", 500


# =========================
# AUTH
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username and password:
            user = authenticate(username, password)
            if user:
                login_user(user)
                return redirect(url_for("index"))
        error = "Benutzername oder Passwort ist falsch."

    return render_template(
        "auth.html",
        title="In dein Konto einloggen",
        action=url_for("login"),
        button_label="Einloggen",
        error=error,
        footer_text="Noch kein Konto?",
        footer_link_url=url_for("register"),
        footer_link_label="Registrieren"
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username and password:
            ok = register_user(username, password)
            if ok:
                return redirect(url_for("login"))
        error = "Benutzername existiert bereits oder Eingaben ungueltig."

    return render_template(
        "auth.html",
        title="Neues Konto erstellen",
        action=url_for("register"),
        button_label="Registrieren",
        error=error,
        footer_text="Du hast bereits ein Konto?",
        footer_link_url=url_for("login"),
        footer_link_label="Einloggen"
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# =========================
# TODO COMPLETE
# =========================
@app.post("/complete")
@login_required
def complete():
    todo_id = request.form.get("id")
    db_write(
        "DELETE FROM todos WHERE user_id=%s AND id=%s",
        (current_user.id, todo_id,)
    )
    return redirect(url_for("index"))


# =========================
# MAINPAGE
# =========================
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    product = None
    alternative = None
    form_type = request.form.get("form_type")

    # BARCODE
    if form_type == "barcode":
        barcode = request.form.get("barcode")
        category_name = BARCODES.get(barcode)

        if category_name:
            product = {
                "name": category_name,
                "materials": CATEGORIES.get(category_name, {}).get("materials", [])
            }

            try:
                current_materials = len([m for m in product["materials"] if m.get("present", False)])
                alternatives = []
                for name, data in CATEGORIES.items():
                    if name != category_name:
                        alt_materials = len([m for m in data.get("materials", []) if m.get("present", False)])
                        if alt_materials < current_materials:
                            alternatives.append((name, alt_materials))
                if alternatives:
                    alternative = min(alternatives, key=lambda x: x[1])
            except Exception as e:
                logging.debug("Fehler bei Alternativ-Berechnung: %s", e)
                alternative = None
        else:
            product = {"name": "Unbekanntes Produkt", "materials": []}

    # TODO
    elif form_type == "todo":
        content = request.form.get("contents")
        due = request.form.get("due_at")

        if content and due:
            db_write(
                "INSERT INTO todos (user_id, content, due) VALUES (%s, %s, %s)",
                (current_user.id, content, due)
            )
        return redirect(url_for("index"))

    # TODOS LADEN
    todos = db_read(
        "SELECT id, content, due FROM todos WHERE user_id=%s ORDER BY due",
        (current_user.id,)
    )

    # due_text fuer Template (weil SQLite due als Text liefert)
    for t in todos:
        # Minimal robust: falls due None ist
        t["due_text"] = t.get("due") or "-"

    return render_template(
        "main_page.html",
        todos=todos,
        product=product,
        alternative=alternative
    )


# =========================
# POINTS PAGE
# =========================
@app.route("/points", methods=["GET", "POST"])
@login_required
def points_page():
    if request.method == "POST":
        waste = request.form.get("waste", "").lower()
        if waste in POINTS_PER_WASTE:
            add_user_points(current_user.id, POINTS_PER_WASTE[waste])
        return redirect(url_for("points_page"))

    user_points = get_user_points(current_user.id)
    return render_template("pluspoint_page.html", points=user_points, points_per_waste=POINTS_PER_WASTE)


# =========================
# CATEGORIES PAGE
# =========================
@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories_page():
    return render_template("categories.html", categories=CATEGORIES)


# =========================
# API FUER DIE KARTE
# =========================
@app.route("/entsorgung")
def entsorgung():
    # Dummy Daten (dein JS erwartet data.elements)
    return jsonify({
        "elements": [
            {"lat": 47.3769, "lon": 8.5417},
            {"lat": 47.3725, "lon": 8.5346},
            {"lat": 47.3800, "lon": 8.5300}
        ]
    })


# =========================
if __name__ == "__main__":
    app.run()
