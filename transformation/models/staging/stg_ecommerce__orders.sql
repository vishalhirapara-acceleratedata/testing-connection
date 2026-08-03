with source as (
    select * from {{ ref('orders') }}
),

renamed as (
    select
        cast(order_id as integer) as order_id,
        cast(customer_id as integer) as customer_id,
        cast(order_date as date) as order_date,
        cast(status as varchar) as status,
        cast(total_amount as double) as total_amount,
        cast(shipping_address_id as integer) as shipping_address_id
    from source
)

select * from renamed
