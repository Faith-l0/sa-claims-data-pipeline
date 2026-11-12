-- 1. Total Claim Exposure & Average Claim Value by Province
SELECT 
    province,
    COUNT(*) AS total_claims,
    ROUND(SUM(claim_amount_zar), 2) AS total_exposure_zar,
    ROUND(AVG(claim_amount_zar), 2) AS avg_claim_zar
FROM clean_claims
GROUP BY province
ORDER BY total_exposure_zar DESC;

-- 2. Approval Rate & Average Reporting Lag by Claim Type
SELECT 
    claim_type,
    COUNT(*) AS claim_volume,
    ROUND(AVG(days_to_report), 1) AS avg_days_to_report,
    ROUND(100.0 * SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) / COUNT(*), 1) AS approval_rate_pct
FROM clean_claims
GROUP BY claim_type
ORDER BY approval_rate_pct DESC;

-- 3. High-Value Outlier Detection (Claims exceeding R500,000 for Senior Risk Review)
SELECT 
    claim_id,
    policy_holder_id,
    province,
    claim_type,
    claim_amount_zar,
    status
FROM clean_claims
WHERE claim_amount_zar > 500000
ORDER BY claim_amount_zar DESC;

-- 4. Data Governance Audit Summary
SELECT 
    issue_type,
    COUNT(*) AS flagged_records
FROM audit_exceptions
GROUP BY issue_type;
