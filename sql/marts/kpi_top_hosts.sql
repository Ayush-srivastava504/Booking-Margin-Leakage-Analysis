CREATE TABLE kpi_top_hosts AS
SELECT 
    host_id,
    COUNT(*) AS bookings,
    ROUND(SUM(net_host_margin), 0) AS total_margin,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct,
    ROUND(SUM(is_cancelled) * 100.0 / COUNT(*), 1) AS cancel_rate_pct
FROM int_booking_margins
GROUP BY host_id
ORDER BY total_margin DESC
LIMIT 10;