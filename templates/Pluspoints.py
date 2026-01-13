from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

points = 0


POINTS_PER_WASTE = {
    "pet": 5,
    "glas": 3,
    "papier": 2
}

@app.route("/", methods=["GET", "POST"])
def home():
    global points

    if request.method == "POST":
        waste = request.form.get("waste")
        if waste in POINTS_PER_WASTE:
            points += POINTS_PER_WASTE[waste]
        return redirect(url_for("home"))

    return render_template("home_page.html", points=points)

if __name__ == "__main__":
    app.run(debug=True)

