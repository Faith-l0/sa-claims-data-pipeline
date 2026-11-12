# South African Insurance Claims ETL & Risk Audit Pipeline

An end-to-end **Python and SQLite data pipeline** designed to ingest, validate, clean, and analyze insurance claims data while enforcing automated data-governance and audit controls.

## Project Overview
In high-volume insurance operations (such as First Notice of Loss processing), incoming records frequently contain missing fields, duplicate identifiers, or chronological errors. This project simulates a realistic 500-record South African claims dataset, applies automated validation rules to quarantine anomalies, loads clean records into a relational SQLite data warehouse, and executes analytical SQL queries for risk and operational reporting.

## Architecture & Pipeline Flow
1. **Data Simulation (`generate_claims.py`):** Generates 500 synthetic South African insurance claims across multiple provinces and claim categories, intentionally injecting real-world data quality issues (duplicate IDs, missing/abbreviated province codes, negative amounts, and dates where the report precedes the incident).
2. **ETL & Governance Audit (`claims_etl.py`):**
   - **Standardization:** Normalizes inconsistent region values (e.g., mapping WC to Western Cape and handling null values).
   - **Audit Exception Logging:** Quarantines invalid records into an `audit_exceptions` table with specific error classifications rather than silently dropping data.
   - **Warehouse Loading:** Loads validated records into a normalized `clean_claims` SQLite table with calculated reporting-lag metrics (`days_to_report`).
3. **Business Intelligence & Risk Queries (`queries.sql`):**
   - Total financial exposure and average claim value by province.
   - Claim approval rates and average reporting lag across claim types.
   - High-value outlier detection (flagging claims exceeding R500,000 for senior risk review).
   - Summary audit breakdown of quarantined data anomalies.

## Tech Stack
- **Language:** Python 3 (`csv`, `sqlite3`, `datetime`, `random`)
- **Database & Querying:** SQLite, SQL
- **Environment:** Linux (Ubuntu)

## How to Run Locally
1. Clone the repository: `git clone https://github.com/Faith-l0/sa-claims-data-pipeline.git`
2. Navigate into the folder: `cd sa-claims-data-pipeline`
3. Generate raw data: `python3 generate_claims.py`
4. Run ETL pipeline: `python3 claims_etl.py`
5. Run SQL analytics: `sqlite3 -header -column claims_warehouse.db < queries.sql`

## Pipeline Results
- **Records Processed:** 500 raw records
- **Clean Warehouse Records:** 492 validated claims loaded into `clean_claims`
- **Governance Exceptions Flagged:** 8 anomalies isolated in `audit_exceptions` (3 duplicate claim IDs, 3 chronological date errors, and 2 negative financial entries)
