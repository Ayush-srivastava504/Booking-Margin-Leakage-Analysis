CREATE TABLE kpi_cancellation_impact AS
SELECT 
    booking_window,
    COUNT(*) AS bookings,
    SUM(is_cancelled) AS cancelled_count,
    ROUND(SUM(is_cancelled) * 100.0 / COUNT(*), 1) AS cancel_rate_pct,
    ROUND(SUM(CASE WHEN is_cancelled = 1 THEN net_host_margin ELSE 0 END), 0) AS margin_lost,
    ROUND(AVG(CASE WHEN is_cancelled = 0 THEN net_host_margin END), 2) AS avg_margin_completed
FROM int_booking_margins
GROUP BY booking_window
ORDER BY cancel_rate_pct DESC;