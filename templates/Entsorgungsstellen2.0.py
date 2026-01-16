import pandas as pd
import requests
import folium

# ——————————————————————————————
# 1) Lade aktuelle Position über IP
# ——————————————————————————————

def get_current_location():
    try:
        # IP-Geodatendienst (frei)
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        
        if "loc" in data:
            lat, lon = map(float, data["loc"].split(","))
            return lat, lon
    except Exception as e:
        print("Fehler beim Standort: ", e)
    return None, None

# ——————————————————————————————
# 2) Lade Entsorgungsstellen
# ——————————————————————————————

def load_disposal_sites(csv_path):
    df = pd.read_csv(csv_path)
    # Erwartete Spalten in CSV: latitude, longitude, name
    return df

# ——————————————————————————————
# 3) Karte erstellen
# ——————————————————————————————

def create_map(disposal_csv):
    # aktueller Standort
    my_lat, my_lon = get_current_location()
    
    # Lade Entsorgungsstellen
    df_sites = load_disposal_sites(disposal_csv)

    # Karte zentriert in Zürich
    start_coords = (47.3769, 8.5417)
    fmap = folium.Map(location=start_coords, zoom_start=12)

    # Marker: eigene Position
    if my_lat and my_lon:
        folium.Marker(
            location=(my_lat, my_lon),
            popup="🔵 Du bist hier",
            icon=folium.Icon(color="blue", icon="user")
        ).add_to(fmap)

    # Marker: Entsorgungsstellen
    for _, row in df_sites.iterrows():
        folium.Marker(
            location=(row["latitude"], row["longitude"]),
            popup=row.get("name", "Entsorgungsstelle"),
            icon=folium.Icon(color="green", icon="recycle")
        ).add_to(fmap)

    # Speichere Map
    fmap.save("entsorgung_karte.html")
    print("Karte erstellt: entsorgung_karte.html ✔️")

# ——————————————————————————————
# 4) Ausführen
# ——————————————————————————————

if __name__ == "__main__":
    create_map("entsorgungsstellen_zurich.csv")
