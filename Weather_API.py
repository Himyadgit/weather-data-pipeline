import requests
import pandas as pd
import os
import sys

# ==============================
# Configuration
# ==============================
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
if not API_KEY:
    print("❌ ERROR: OPEN_WEATHER_API_KEY environment variable not set")
    sys.exit(1)

URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

# ==============================
# Fetch weather data
# ==============================
records = []

for city in CITIES:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(URL, params=params)

    if response.status_code != 200:
        print(f"❌ Failed for {city} | Status: {response.status_code}")
        continue

    data = response.json()

    records.append({
        "city": city,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["main"],
        "wind_speed": data["wind"]["speed"]
    })

print("✅ Weather data fetched successfully")

# ==============================
# Create DataFrame
# ==============================
weather_df = pd.DataFrame(records)

if weather_df.empty:
    print("❌ No data collected. Exiting.")
    sys.exit(1)

print(weather_df)

# ==============================
# Save for Power BI
# ==============================
output_path = r"C:\Users\yhima\Desktop\power bi test\weather_pipeline\Data\Weather.csv"
weather_df.to_csv(output_path, index=False)

print(f"✅ Data saved to: {output_path}")

# ==============================
# Analytics
# ==============================
avg_temp = weather_df["temperature"].mean()
hottest_city = weather_df.loc[weather_df["temperature"].idxmax(), "city"]
weather_count = weather_df["weather"].value_counts()

print("\n📊 Summary")
print("Average Temp:", round(avg_temp, 2))
print("Hottest City:", hottest_city)
print(weather_count)
