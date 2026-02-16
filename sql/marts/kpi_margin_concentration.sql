CREATE TABLE kpi_margin_concentration AS
WITH ranked AS (
    SELECT 
        host_id,
        SUM(net_host_margin) AS host_margin,
        ROW_NUMBER() OVER(ORDER BY SUM(net_host_margin) DESC) AS rank
    FROM int_booking_margins
    GROUP BY host_id
),
totals AS (
    SELECT SUM(net_host_margin) AS total FROM int_booking_margins
)
SELECT 
    'Top 20% hosts' AS segment,
    ROUND(SUM(host_margin) * 100 / (SELECT total FROM totals), 1) AS pct_of_margin,
    COUNT(*) AS num_hosts
FROM ranked, totals
WHERE rank <= (SELECT COUNT(*) * 0.20 FROM ranked);