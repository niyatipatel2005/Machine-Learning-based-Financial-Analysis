# scripts/extract_metrics.py

import json
import os

INPUT_DIR = "../raw_data"
OUTPUT_DIR = "../metrics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_metrics(company_id):
    filepath = f"{INPUT_DIR}/{company_id}.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    
    company_data = data.get("data", {})
    pl_data = company_data.get("profitandloss", [])
    
    filtered = [row for row in pl_data if row["year"].startswith("Mar")]
    filtered.sort(key=lambda x: x["year"])
    
    metrics = {"company_id": company_id}

    def cagr(start, end, years):
        try:
            return round(((end / start) ** (1 / years) - 1) * 100, 2)
        except:
            return 0.0

    def get_growth(field, period):
        if len(filtered) < period + 1:
            return 0.0
        start = filtered[-(period + 1)].get(field, 0)
        end = filtered[-1].get(field, 0)
        return cagr(start, end, period)

    metrics["roe"] = float(data.get("company", {}).get("roe_percentage", 0))
    metrics["sales_3y"] = get_growth("sales", 3)
    metrics["sales_5y"] = get_growth("sales", 5)
    metrics["sales_10y"] = get_growth("sales", 10)
    metrics["profit_3y"] = get_growth("net_profit", 3)
    metrics["profit_5y"] = get_growth("net_profit", 5)
    metrics["profit_10y"] = get_growth("net_profit", 10)

    return metrics

def save_metrics(company_id, metrics):
    filepath = f"{OUTPUT_DIR}/{company_id}.json"
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"[✅] Metrics saved to {filepath}")

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    print(f"🔍 Found {len(files)} company files in raw_data")

    for idx, filename in enumerate(files, start=1):
        company_id = filename.replace(".json", "")
        try:
            print(f"({idx}/{len(files)}) Extracting metrics for: {company_id}")
            metrics = extract_metrics(company_id)
            save_metrics(company_id, metrics)
        except Exception as e:
            print(f"[⚠️] Failed for {company_id}: {e}")

if __name__ == "__main__":
    main()
