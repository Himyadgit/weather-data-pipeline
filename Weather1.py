# %%
import requests
import pandas as pd
import os
from datetime import datetime

# Read API key from environment variable
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

# API endpoint
url = "https://api.openweathermap.org/data/2.5/weather"

# Cities list
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

records = []

print("🌦️ Weather data fetching started...")

for city in cities:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        records.append({
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now()
        })
    else:
        print(f"❌ Failed for {city}: {response.status_code}")

# Create DataFrame
weather_df = pd.DataFrame(records)

# Ensure Data folder exists
os.makedirs("data", exist_ok=True)

# Save to CSV
output_path = "data/Weather.csv"
#output_path = r"C:\Users\yhima\Desktop\power bi test\weather_pipeline\data\Weather.csv"
weather_df.to_csv(output_path, index=False)

print("✅ Weather data fetched and saved successfully")


