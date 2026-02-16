CREATE TABLE kpi_revenue_overview AS
SELECT 
    COUNT(*) AS total_bookings,
    COUNT(DISTINCT host_id) AS num_hosts,
    ROUND(SUM(gross_booking_value), 0) AS total_gbv,
    ROUND(AVG(gross_booking_value), 2) AS avg_booking_value,
    ROUND(SUM(net_host_margin), 0) AS total_net_margin,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct
FROM int_booking_margins;