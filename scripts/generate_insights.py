# scripts/generate_insights.py

import json
import os

INPUT_DIR = "../metrics"
OUTPUT_DIR = "../insights"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_metrics(company_id):
    filepath = f"{INPUT_DIR}/{company_id}.json"
    with open(filepath, "r") as f:
        return json.load(f)

def generate_insights(metrics):
    company_id = metrics["company_id"]
    pros = []
    cons = []

    # ROE
    if metrics["roe"] >= 10:
        pros.append(f"Company has a good return on equity (ROE) track record: {metrics['roe']}%")
    else:
        cons.append(f"Company has a low return on equity of {metrics['roe']}% over last 3 years.")

    # Profit Growth
    for period in [3, 5, 10]:
        value = metrics[f"profit_{period}y"]
        if value > 10:
            pros.append(f"Company has delivered good profit growth of {value}% over {period} years.")
        else:
            cons.append(f"Company has delivered poor profit growth of {value}% over {period} years.")

    # Sales Growth
    for period in [3, 5, 10]:
        value = metrics[f"sales_{period}y"]
        if value > 10:
            pros.append(f"Company's median sales growth is {value}% over {period} years.")
        else:
            cons.append(f"Company has delivered poor sales growth of {value}% over {period} years.")

    # Keep top 3 only
    return {
        "company_id": company_id,
        "pros": pros[:3],
        "cons": cons[:3]
    }

def save_insights(company_id, insights):
    filepath = f"{OUTPUT_DIR}/{company_id}.json"
    with open(filepath, "w") as f:
        json.dump(insights, f, indent=4)
    print(f"[✅] Insights saved to {filepath}")

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    print(f"🧠 Generating insights for {len(files)} companies")

    for idx, filename in enumerate(files, start=1):
        company_id = filename.replace(".json", "")
        try:
            metrics = load_metrics(company_id)
            insights = generate_insights(metrics)
            save_insights(company_id, insights)
        except Exception as e:
            print(f"[⚠️] Failed for {company_id}: {e}")

    print("\n✅ Done generating all insights.")

if __name__ == "__main__":
    main()
