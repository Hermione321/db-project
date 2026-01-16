# Diese Datei ist deprecated
# Die Funktionalität wurde in flask_app.py integriert
# Die Punkte-Seite ist jetzt unter /points erreichbar
# und speichert Punkte benutzer-spezifisch in der Datenbank

# Nur für direktes Ausführen - startet die Hauptapp
if __name__ == "__main__":
    from flask_app import app
    app.run(debug=True)
