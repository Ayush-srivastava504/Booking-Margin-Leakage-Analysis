CREATE TABLE kpi_cost_breakdown AS
SELECT 
    ROUND(AVG(cleaning_cost), 2) AS avg_cleaning,
    ROUND(AVG(supplies_cost), 2) AS avg_supplies,
    ROUND(AVG(maintenance_allocation), 2) AS avg_maintenance,
    ROUND(AVG(total_host_costs), 2) AS avg_total_costs,
    ROUND(SUM(cleaning_cost) * 100.0 / SUM(gross_booking_value), 2) AS cleaning_pct,
    ROUND(SUM(supplies_cost) * 100.0 / SUM(gross_booking_value), 2) AS supplies_pct,
    ROUND(SUM(maintenance_allocation) * 100.0 / SUM(gross_booking_value), 2) AS maintenance_pct,
    ROUND(SUM(total_host_costs) * 100.0 / SUM(gross_booking_value), 2) AS total_costs_pct
FROM int_booking_margins;