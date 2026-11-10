"""
OpenAQ Chennai Air Quality Data Collector - Enhanced Version
Fetches ALL available 2024-2025 data from Chennai stations
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time

BASE_URL = "https://api.openaq.org/v3"
API_KEY = "d816dddcc41b9c09f8ca8ca1bb816fc39f161e2f8063b0fc3e8e045674670cbe"

headers = {
    "X-API-Key": API_KEY,
    "Accept": "application/json"
}

# Target parameters
PARAMETERS = ['PM10','PM2.5','NO2','SO2','CO','O3 MASS']

# Date range - specifically for 2024
DATE_FROM = "2026-02-01"
DATE_TO = "2026-02-28"

# Station IDs that have data from before 2025 (based on API check)
CHENNAI_STATIONS = {
11581	:"Arumbakkam, Chennai - TNPCB",
11579	:"Kodungaiyur, Chennai - TNPCB",
6920	:"Manali Village, Chennai - TNPCB",
10780	:"Manali Village, Chennai - TNPCB",
2586	:"Manali, Chennai - CPCB",
12046	:"Perungudi, Chennai - TNPCB",
11578	:"Royapuram, Chennai - TNPCB",
5655	:"Velachery Res. Area, Chennai - CPCB"

    }


def get_sensors_for_location(location_id):
    """Get all sensors for a location"""
    url = f"{BASE_URL}/locations/{location_id}/sensors"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"  Error fetching sensors: {response.status_code}")
        return []
    
    return response.json().get("results", [])


def get_sensor_days(sensor_id, date_from, date_to):
    """Get daily measurements for a sensor with chunking for reliability"""
    all_data = []
    
    # Break into monthly chunks
    start = datetime.strptime(date_from, "%Y-%m-%d")
    end = datetime.strptime(date_to, "%Y-%m-%d")
    
    current = start
    while current < end:
        chunk_end = min(current + timedelta(days=31), end)
        
        url = f"{BASE_URL}/sensors/{sensor_id}/days"
        params = {
            "date_from": current.strftime("%Y-%m-%d"),
            "date_to": chunk_end.strftime("%Y-%m-%d"),
            "limit": 1000
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                results = response.json().get("results", [])
                all_data.extend(results)
        except Exception as e:
            print(f"    Error: {e}")
        
        current = chunk_end + timedelta(days=1)
        time.sleep(0.3)
    
    return all_data


def collect_2025_data():
    """Collect 2024 data from all Chennai stations"""
    all_data = []
    
    for loc_id, loc_name in CHENNAI_STATIONS.items():
        print(f"\n{'='*60}")
        print(f"Station: {loc_name} (ID: {loc_id})")
        print(f"{'='*60}")
        
        # Get sensors
        sensors = get_sensors_for_location(loc_id)
        print(f"Found {len(sensors)} sensors")
        
        for sensor in sensors:
            sensor_id = sensor.get("id")
            param = sensor.get("parameter", {})
            param_name = param.get("name", "").lower()
            param_display = param.get("displayName", param_name)
            units = param.get("units", "")
            
            # Only collect target parameters (pollutants instead of weather)
            pollutant_params = [p.lower() for p in PARAMETERS]

            if not any(p in param_name for p in pollutant_params):
                continue
            
            # Normalize display name
            param_display_safe = param_display.replace("\u2082", "2").replace("\u2083", "3").replace("\u2081\u2080", "10")
            print(f"  Fetching {param_display_safe} (Sensor ID: {sensor_id})...")
            
            measurements = get_sensor_days(sensor_id, DATE_FROM, DATE_TO)
            print(f"    -> Got {len(measurements)} days")
            
            for meas in measurements:
                period = meas.get("period", {})
                dt_from = period.get("datetimeFrom", {})
                date_str = dt_from.get("local", "")[:10] if dt_from else ""
                
                if not date_str:
                    continue
                
                all_data.append({
                    "Date": date_str,
                    "Station": loc_name,
                    "Location_ID": loc_id,
                    "Parameter": param_display_safe.upper(),
                    "Value": meas.get("value"),
                    "Units": units
                })
            
            time.sleep(0.3)
    
    return all_data


def main():
    print("=" * 70)
    print("OpenAQ Chennai 2025 Data Collection - Enhanced")
    print("=" * 70)
    print(f"Date range: {DATE_FROM} to {DATE_TO}")
    print(f"Stations: {len(CHENNAI_STATIONS)}")
    print("=" * 70)
    
    # Collect data
    all_data = collect_2025_data()
    
    if not all_data:
        print("\nNo data collected!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    print(f"\nRaw data collected: {len(df)} records")
    
    # Pivot to wide format
    df_pivot = df.pivot_table(
        index=["Date", "Station", "Location_ID",'Units'],
        columns="Parameter",
        values="Value",
        aggfunc="mean"
    ).reset_index()
    
    df_pivot = df_pivot.sort_values(["Date", "Station"])
    
    # Save
    output_file = "chennai_feb_data.csv"
    df_pivot.to_csv(output_file, index=False)
    
    print(f"\n{'=' * 70}")
    print(f"SUCCESS! Saved to {output_file}")
    print(f"Total rows: {len(df_pivot)}")
    print(f"Date range: {df_pivot['Date'].min()} to {df_pivot['Date'].max()}")
    print(f"{'=' * 70}")
    
    # Show breakdown by station
    print("\nData per station:")
    for station in df_pivot['Station'].unique():
        count = len(df_pivot[df_pivot['Station'] == station])
        print(f"  {station}: {count} days")
    


if __name__ == "__main__":
    main()
