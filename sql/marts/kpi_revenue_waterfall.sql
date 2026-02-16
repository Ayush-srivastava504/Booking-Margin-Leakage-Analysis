CREATE TABLE kpi_revenue_waterfall AS
SELECT 'GBV' AS item, ROUND(SUM(gross_booking_value), 0) AS amount, 100 AS pct
FROM int_booking_margins
UNION ALL
SELECT 'Platform Fees', ROUND(SUM(total_platform_fees), 0),
    ROUND(SUM(total_platform_fees) * 100 / SUM(gross_booking_value), 1)
FROM int_booking_margins
UNION ALL
SELECT 'Payment Fees', ROUND(SUM(payment_processing_fee), 0),
    ROUND(SUM(payment_processing_fee) * 100 / SUM(gross_booking_value), 1)
FROM int_booking_margins
UNION ALL
SELECT 'Host Costs', ROUND(SUM(total_host_costs), 0),
    ROUND(SUM(total_host_costs) * 100 / SUM(gross_booking_value), 1)
FROM int_booking_margins
UNION ALL
SELECT 'Net Margin', ROUND(SUM(net_host_margin), 0),
    ROUND(SUM(net_host_margin) * 100 / SUM(gross_booking_value), 1)
FROM int_booking_margins;