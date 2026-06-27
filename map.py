from flask import Flask, render_template
import pandas as pd
import re

app = Flask(__name__)

def convert_to_decimal(coord):
    match = re.match(r"(\d+)°([\d\.]+)", str(coord))
    if match:
        degree = float(match.group(1))
        minutes = float(match.group(2))
        return degree + (minutes / 60)
    return None

@app.route("/")
def home():
    return "Home working"

@app.route("/map")
def map_view():
    return render_template("map.html")

@app.route("/map-data")
def map_data():
    df = pd.read_csv("groundwater_cleaned.csv")

    data = []
    for _, row in df.iterrows():
        lat = convert_to_decimal(row["latitude"])
        lng = convert_to_decimal(row["longitude"])

        if lat is not None and lng is not None:
            data.append({
                "lat": lat,
                "lng": lng,
                "station": row["stn_name"]
            })

    return {"data": data}

if __name__ == "__main__":
    app.run(debug=True)