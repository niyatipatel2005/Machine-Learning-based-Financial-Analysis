from flask import Blueprint, render_template, request
import mysql.connector
import os
import json

main = Blueprint("main", __name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Use your actual password
        database="ml"
    )

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/company")
def company():
    company_id = request.args.get("id", "").upper().strip()

    if not company_id:
        return render_template("company.html", company_id="", pros=[], cons=[], metrics={})

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT pros, cons FROM prosandcons WHERE company_id = %s", (company_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        pros = [row["pros"] for row in rows if row["pros"]]
        cons = [row["cons"] for row in rows if row["cons"]]

        # Load metrics JSON
        metrics_path = f"metrics/{company_id}.json"
        if os.path.exists(metrics_path):
            with open(metrics_path) as f:
                metrics = json.load(f)
        else:
            metrics = {}

        return render_template("company.html", company_id=company_id, pros=pros, cons=cons, metrics=metrics)

    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL Error: {err}")
        return render_template("company.html", company_id=company_id, pros=[], cons=[], metrics={}, error="Database error.")
