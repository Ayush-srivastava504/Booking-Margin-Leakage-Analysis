CREATE TABLE kpi_room_type_performance AS
SELECT 
    room_type,
    COUNT(*) AS bookings,
    COUNT(DISTINCT host_id) AS num_hosts,
    ROUND(AVG(gross_booking_value), 2) AS avg_gbv,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct,
    ROUND(SUM(is_cancelled) * 100.0 / COUNT(*), 1) AS cancel_rate_pct,
    ROUND(SUM(net_host_margin), 0) AS total_margin
FROM int_booking_margins
GROUP BY room_type
ORDER BY avg_margin_pct DESC;