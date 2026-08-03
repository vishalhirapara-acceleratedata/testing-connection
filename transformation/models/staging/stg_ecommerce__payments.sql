with source as (
    select * from {{ ref('payments') }}
),

renamed as (
    select
        cast(payment_id as integer) as payment_id,
        cast(order_id as integer) as order_id,
        cast(payment_date as timestamp) as payment_date,
        cast(amount as double) as amount,
        cast(method as varchar) as method,
        cast(status as varchar) as status
    from source
)

select * from renamed
