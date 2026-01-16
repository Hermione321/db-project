from flask import Flask, render_template

app = Flask(__name__)

# Beispiel-Daten (kann später durch echte API ersetzt werden)
entsorgungsstellen = [
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Merkurstrasse, 8032 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Recyclinghof Werdhölzli",
        "adresse": "Bändlistrasse 94, 8064 Zürich",
        "typ": "Sonderabfälle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Am Schanzengraben 25, 8002 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Aegertenstrasse 16, 8003 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Seebahnstrasse 89, 8003 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Konradstrasse 79, 8005 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Neugasse 116, 8005 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Tellstrasse 38, 8004 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "zsge Recycling Werkstatt und Sammelstelle für Elektroschrott",
        "adresse": "Kanonengasse 20, 8004 Zürich",
        "typ": "Recycling Werkstatt und Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Hardstrasse 9, 8004 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Zimmerlistrasse 2, 8004 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Spross Recyclingwerk Zürich",
        "adresse": "Hohlstrasse 330, 8004 Zürich",
        "typ": "Recyclingwerk"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Heinrichstrasse 191, 8005 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "8006 Zürich",
        "typ": "Sammelstelle"
    },
    {
        "name": "Wertstoff-Sammelstelle",
        "adresse": "Klopstockstrasse 23, 8002 Zürich",
        "typ": "Sammelstelle"
    }
]

@app.route("/")
def index():
    return render_template("index.html", stellen=entsorgungsstellen)

if __name__ == "__main__":
    app.run(debug=True)
