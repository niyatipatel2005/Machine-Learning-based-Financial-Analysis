# scripts/insert_to_mysql.py

import json
import os
import mysql.connector

INSIGHTS_DIR = "../insights"

# === MySQL Configuration ===
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # XAMPP default has no password
    "database": "ml"
}

def insert_insight(cursor, company_id, pros, cons):
    query = """
    INSERT INTO prosandcons (company_id, pros, cons)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (company_id, pros, cons))

def main():
    files = [f for f in os.listdir(INSIGHTS_DIR) if f.endswith(".json")]
    if not files:
        print("❌ No insight files found in 'insights' folder.")
        return

    print(f"📦 Inserting insights for {len(files)} companies...\n")

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        for idx, filename in enumerate(files, start=1):
            filepath = os.path.join(INSIGHTS_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)

            company_id = data.get("company_id")
            pros = data.get("pros", [])
            cons = data.get("cons", [])

            for p in pros:
                insert_insight(cursor, company_id, p, None)
            for c in cons:
                insert_insight(cursor, company_id, None, c)

            print(f"({idx}/{len(files)}) ✅ Inserted insights for {company_id}")

        connection.commit()
        print("\n✅ All insights inserted into MySQL!")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
