with source as (
    select * from {{ ref('coupons') }}
),

renamed as (
    select
        cast(coupon_id as integer) as coupon_id,
        cast(code as varchar) as code,
        cast(discount_type as varchar) as discount_type,
        cast(discount_value as double) as discount_value,
        cast(min_order_amount as double) as min_order_amount,
        cast(expires_at as date) as expires_at
    from source
)

select * from renamed
