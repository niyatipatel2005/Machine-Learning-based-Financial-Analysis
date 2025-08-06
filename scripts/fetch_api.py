# scripts/fetch_api.py

import os
import pandas as pd
import requests
import json
import time

# === Constants ===
API_KEY = "ghfkffu6378382826hhdjgk"
BASE_URL = "https://bluemutualfund.in/server/api/company.php"
RAW_DATA_DIR = "../raw_data"  # Ensure this is at the root level

# === Load Company List from Excel ===
def load_company_list(filepath):
    df = pd.read_excel(filepath)
    return df["company_id"].dropna().tolist()

# === API Call Function ===
def fetch_data_for_company(company_id):
    params = {
        "id": company_id,
        "api_key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed for {company_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Error for {company_id}: {e}")
        return None

# === Save JSON to raw_data/ ===
def save_raw_data(company_id, data):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filepath = os.path.join(RAW_DATA_DIR, f"{company_id}.json")
    
    if os.path.exists(filepath):
        print(f"[SKIP] {company_id}.json already exists.")
        return

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
        print(f"[OK] Data saved for {company_id}")

# === Main Runner ===
def main():
    excel_path = "C:\\Users\\hp\\Documents\\BLUESTOCK\\ML_Financial_Analysis\\assets\\company_id.xlsx"
    company_list = load_company_list(excel_path)

    print(f"📊 Total Companies to Fetch: {len(company_list)}")
    print(f"📁 Saving to folder: {RAW_DATA_DIR}\n")

    for idx, company_id in enumerate(company_list, start=1):
        print(f"({idx}/{len(company_list)}) Fetching data for: {company_id}")
        data = fetch_data_for_company(company_id)
        if data:
            save_raw_data(company_id, data)
        time.sleep(1)  # ⏳ delay to avoid API rate limits

    print("\n✅ Done fetching all companies.")

# === Entry Point ===
if __name__ == "__main__":
    main()
