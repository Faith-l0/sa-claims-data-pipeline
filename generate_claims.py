import csv
import random
from datetime import datetime, timedelta

provinces = ["Western Cape", "Gauteng", "KwaZulu-Natal", "Eastern Cape", "Free State", None, "WC"]
claim_types = ["Motor Accident", "Property Damage", "Theft", "Medical", "Windscreen"]
statuses = ["Approved", "Pending", "Rejected", "Under Investigation"]

random.seed(42)

with open("raw_claims_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "claim_id", "policy_holder_id", "province", "claim_type",
        "incident_date", "reported_date", "claim_amount_zar", "status"
    ])

    base_date = datetime(2026, 1, 1)

    for i in range(1, 501):
        claim_id = f"CLM-{1000 + i}"
        if i in [50, 142, 310]:
            claim_id = f"CLM-{1000 + i - 1}"

        policy_id = f"POL-{random.randint(5000, 5300)}"
        province = random.choice(provinces)
        c_type = random.choice(claim_types)

        inc_date = base_date + timedelta(days=random.randint(0, 280))
        rep_date = inc_date + timedelta(days=random.randint(0, 14))

        if i in [25, 199, 404]:
            rep_date = inc_date - timedelta(days=5)

        amount = round(random.uniform(1500.00, 185000.00), 2)
        if i in [88, 275]:
            amount = -4500.00
        elif i == 350:
            amount = 2500000.00

        status = random.choice(statuses)

        writer.writerow([
            claim_id, policy_id, province, c_type,
            inc_date.strftime("%Y-%m-%d"),
            rep_date.strftime("%Y-%m-%d"),
            amount, status
        ])

print("Generated raw_claims_data.csv with 500 records (including intentional anomalies).")
