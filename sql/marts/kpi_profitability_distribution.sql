CREATE TABLE kpi_profitability_distribution AS
SELECT 
    profitability_status,
    COUNT(*) AS num_bookings,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct,
    ROUND(AVG(net_margin_pct), 2) AS avg_margin_pct
FROM int_booking_margins
GROUP BY profitability_status;