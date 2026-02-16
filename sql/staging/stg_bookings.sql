CREATE TABLE stg_bookings AS
SELECT 
    booking_id,
    listing_id,
    host_id,
    guest_id,
    booking_date,
    checkin_date,
    checkout_date,
    length_of_stay_nights,
    base_price_per_night,
    total_base_price,
    room_type,
    neighborhood,
    is_cancelled,
    days_until_checkin,
    MONTH(checkin_date) AS checkin_month,
    YEAR(checkin_date) AS checkin_year,
    CASE 
        WHEN days_until_checkin < 3 THEN '<3 days'
        WHEN days_until_checkin < 7 THEN '3-7 days'
        WHEN days_until_checkin < 14 THEN '7-14 days'
        WHEN days_until_checkin < 30 THEN '14-30 days'
        ELSE '30+ days'
    END AS booking_window
FROM bookings;