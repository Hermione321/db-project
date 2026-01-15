from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

@app.route("/entsorgung", methods=["GET"])
def entsorgung():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Koordinaten fehlen"}), 400

    query = f"""
    [out:json];
    (
      node(around:3000,{lat},{lon})["amenity"="recycling"];
      way(around:3000,{lat},{lon})["amenity"="recycling"];
      relation(around:3000,{lat},{lon})["amenity"="recycling"];
    );
    out center;
    """

    response = requests.post(OVERPASS_URL, data=query)
    data = response.json()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

