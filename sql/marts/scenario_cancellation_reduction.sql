CREATE TABLE scenario_cancellation_reduction AS
SELECT 
    COUNT(CASE WHEN is_cancelled = 1 THEN 1 END) AS current_cancellations,
    ROUND(COUNT(CASE WHEN is_cancelled = 1 THEN 1 END) * 0.80, 0) AS after_20pct_reduction,
    ROUND(COUNT(CASE WHEN is_cancelled = 1 THEN 1 END) * 0.20, 0) AS prevented_cancellations,
    ROUND(SUM(CASE WHEN is_cancelled = 1 THEN net_host_margin ELSE 0 END), 0) AS margin_currently_lost,
    ROUND(SUM(CASE WHEN is_cancelled = 1 THEN net_host_margin ELSE 0 END) * 0.20, 0) AS margin_recovered
FROM int_booking_margins;