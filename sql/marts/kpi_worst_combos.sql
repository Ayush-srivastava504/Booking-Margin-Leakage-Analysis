CREATE TABLE kpi_worst_combos AS
SELECT 
    room_type,
    neighborhood,
    COUNT(*) AS bookings,
    COUNT(DISTINCT host_id) AS num_hosts,
    ROUND(AVG(gross_booking_value), 2) AS avg_gbv,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct,
    COUNT(CASE WHEN profitability_status = 'Loss' THEN 1 END) AS loss_count
FROM int_booking_margins
GROUP BY room_type, neighborhood
ORDER BY avg_margin_pct ASC
LIMIT 15;