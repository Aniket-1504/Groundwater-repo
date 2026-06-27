import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("groundwater_cleaned.csv")

plt.figure()
plt.plot(df["approx_depth"].head(50))
plt.title("Water Level Trend")
plt.xlabel("Sample Index")
plt.ylabel("Water Level (m)")
plt.show()

import folium
import pandas as pd

df = pd.read_csv("groundwater_cleaned.csv")

m = folium.Map(location=[20.5, 78.9], zoom_start=5)

for _, row in df.iterrows():
    folium.CircleMarker(
        [row["latitude"], row["longitude"]],
        radius=4,
        popup=f"WQI: {row['wqi']}",
    ).add_to(m)

m.save("map.html")
