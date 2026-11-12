import csv
import sqlite3
from datetime import datetime

DB_NAME = "claims_warehouse.db"

def setup_database(conn):
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS clean_claims;
        DROP TABLE IF EXISTS audit_exceptions;

        CREATE TABLE clean_claims (
            claim_id TEXT PRIMARY KEY,
            policy_holder_id TEXT NOT NULL,
            province TEXT NOT NULL,
            claim_type TEXT NOT NULL,
            incident_date TEXT NOT NULL,
            reported_date TEXT NOT NULL,
            days_to_report INTEGER NOT NULL,
            claim_amount_zar REAL NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE audit_exceptions (
            exception_id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT,
            issue_type TEXT NOT NULL,
            raw_record TEXT NOT NULL
        );
    """)
    conn.commit()

def standardize_province(prov):
    if not prov or prov.strip() == "":
        return "Unknown"
    mapping = {"WC": "Western Cape", "GP": "Gauteng", "KZN": "KwaZulu-Natal"}
    return mapping.get(prov.strip(), prov.strip())

def run_pipeline():
    conn = sqlite3.connect(DB_NAME)
    setup_database(conn)
    cursor = conn.cursor()

    seen_ids = set()
    clean_count = 0
    error_count = 0

    with open("raw_claims_data.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cid = row["claim_id"]
            amount = float(row["claim_amount_zar"])
            inc_dt = datetime.strptime(row["incident_date"], "%Y-%m-%d")
            rep_dt = datetime.strptime(row["reported_date"], "%Y-%m-%d")
            days_diff = (rep_dt - inc_dt).days

            if cid in seen_ids:
                cursor.execute(
                    "INSERT INTO audit_exceptions (claim_id, issue_type, raw_record) VALUES (?, ?, ?)",
                    (cid, "Duplicate Claim ID", str(row))
                )
                error_count += 1
                continue

            if days_diff < 0:
                cursor.execute(
                    "INSERT INTO audit_exceptions (claim_id, issue_type, raw_record) VALUES (?, ?, ?)",
                    (cid, "Reported Date Precedes Incident Date", str(row))
                )
                error_count += 1
                continue

            if amount <= 0:
                cursor.execute(
                    "INSERT INTO audit_exceptions (claim_id, issue_type, raw_record) VALUES (?, ?, ?)",
                    (cid, "Negative or Zero Claim Amount", str(row))
                )
                error_count += 1
                continue

            seen_ids.add(cid)
            clean_prov = standardize_province(row["province"])

            cursor.execute("""
                INSERT INTO clean_claims VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cid, row["policy_holder_id"], clean_prov, row["claim_type"],
                row["incident_date"], row["reported_date"], days_diff,
                amount, row["status"]
            ))
            clean_count += 1

    conn.commit()
    conn.close()
    print(f"ETL Complete: {clean_count} clean records loaded | {error_count} audit exceptions flagged.")

if __name__ == "__main__":
    run_pipeline()
