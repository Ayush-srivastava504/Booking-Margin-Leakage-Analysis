CREATE TABLE scenario_price_increase AS
SELECT 
    ROUND(SUM(gross_booking_value), 0) AS current_gbv,
    ROUND(SUM(gross_booking_value) * 1.10, 0) AS gbv_with_10pct_increase,
    ROUND(SUM(gross_booking_value) * 0.10, 0) AS additional_gbv,
    ROUND(SUM(net_host_margin), 0) AS current_margin,
    ROUND(SUM(net_host_margin) * 1.10, 0) AS margin_with_10pct_increase,
    ROUND(SUM(net_host_margin) * 0.10, 0) AS additional_margin
FROM int_booking_margins;