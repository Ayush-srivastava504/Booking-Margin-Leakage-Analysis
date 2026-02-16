CREATE TABLE int_booking_margins AS
SELECT 
    b.booking_id,
    b.listing_id,
    b.host_id,
    b.guest_id,
    b.booking_date,
    b.checkin_date,
    b.checkout_date,
    b.length_of_stay_nights,
    b.base_price_per_night,
    b.room_type,
    b.neighborhood,
    b.is_cancelled,
    b.booking_window,
    b.checkin_month,
    b.checkin_year,
    f.gross_booking_value,
    f.host_platform_fee,
    f.guest_service_fee,
    f.payment_processing_fee,
    f.total_platform_fees,
    f.net_payout_to_host,
    c.cleaning_cost,
    c.supplies_cost,
    c.maintenance_allocation,
    c.total_host_costs,
    ROUND(f.net_payout_to_host - c.total_host_costs, 2) AS net_host_margin,
    ROUND((f.net_payout_to_host - c.total_host_costs) / f.gross_booking_value * 100, 2) AS net_margin_pct,
    CASE 
        WHEN (f.net_payout_to_host - c.total_host_costs) > 0 THEN 'Profitable'
        WHEN (f.net_payout_to_host - c.total_host_costs) = 0 THEN 'Breakeven'
        ELSE 'Loss'
    END AS profitability_status,
    CASE 
        WHEN b.checkin_month IN (6,7,8,12) THEN 'Peak'
        WHEN b.checkin_month IN (3,4,5,9,10) THEN 'Shoulder'
        ELSE 'Low'
    END AS season
FROM stg_bookings b
LEFT JOIN stg_booking_fees f ON b.booking_id = f.booking_id
LEFT JOIN stg_host_costs c ON b.booking_id = c.booking_id;