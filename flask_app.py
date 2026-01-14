from flask import Flask, redirect, render_template, request, url_for
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

# Init flask app
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# Init auth
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================
# PUNKTE-SYSTEM
# =========================
points = 0

POINTS_PER_WASTE = {
    "pet": 5,
    "glas": 3,
    "aluminium": 2,
    "tetrapak": 1
}


# DON'T CHANGE
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


# DON'T CHANGE
@app.post('/update_server')
def webhook():
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if not x_hub_signature or not W_SECRET:
        return 'Unauthorized', 401

    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo('./mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    return 'Unauthorized', 401


# =========================
# AUTH
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = authenticate(
            request.form["username"],
            request.form["password"]
        )
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
        username = request.form["username"]
        password = request.form["password"]
        ok = register_user(username, password)
        if ok:
            return redirect(url_for("login"))
        error = "Benutzername existiert bereits."

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
    form_type = request.form.get("form_type")

    # BARCODE
    if form_type == "barcode":
        barcode = request.form.get("barcode")
        category_name = BARCODES.get(barcode)

        if category_name:
            product = {
                "name": category_name,
                "materials": CATEGORIES.get(category_name, [])
            }
        else:
            product = {
                "name": "Unbekanntes Produkt",
                "materials": []
            }

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

    return render_template(
        "main_page.html",
        todos=todos,
        product=product
    )


# =========================
# POINTS PAGE
# =========================
@app.route("/points", methods=["GET", "POST"])
@login_required
def points_page():
    global points

    if request.method == "POST":
        waste = request.form.get("waste", "").lower()
        if waste in POINTS_PER_WASTE:
            points += POINTS_PER_WASTE[waste]
        return redirect(url_for("points_page"))

    return render_template("points.html", points=points)

@app.route("/points", methods=["GET", "POST"])
def points_page():
    global points

    if request.method == "POST":
        waste = request.form.get("waste", "").lower()
        if waste in POINTS_PER_WASTE:
            points += POINTS_PER_WASTE[waste]
        return redirect(url_for("points_page"))

    return render_template("points_page.html", points=points)



# =========================
if __name__ == "__main__":
    app.run()
