CREATE TABLE stg_booking_fees AS
SELECT 
    booking_id,
    gross_booking_value,
    base_price,
    cleaning_fee_fixed,
    host_platform_fee,
    guest_service_fee,
    payment_processing_fee,
    net_payout_to_host,
    ROUND(host_platform_fee + guest_service_fee, 2) AS total_platform_fees
FROM booking_fees;