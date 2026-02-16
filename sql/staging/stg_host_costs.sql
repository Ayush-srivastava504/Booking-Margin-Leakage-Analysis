CREATE TABLE stg_host_costs AS
SELECT 
    booking_id,
    cleaning_cost,
    supplies_cost,
    maintenance_allocation,
    total_host_costs
FROM host_costs;