CREATE TABLE kpi_seasonality AS
SELECT 
    season,
    checkin_month AS month,
    COUNT(*) AS bookings,
    ROUND(AVG(gross_booking_value), 2) AS avg_gbv,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct,
    ROUND(SUM(net_host_margin), 0) AS total_margin
FROM int_booking_margins
GROUP BY season, checkin_month
ORDER BY checkin_month;