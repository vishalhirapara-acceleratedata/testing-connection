with source as (
    select * from {{ ref('order_coupons') }}
),

renamed as (
    select
        cast(order_coupon_id as integer) as order_coupon_id,
        cast(order_id as integer) as order_id,
        cast(coupon_id as integer) as coupon_id,
        cast(discount_amount as double) as discount_amount
    from source
)

select * from renamed
