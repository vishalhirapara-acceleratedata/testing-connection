with source as (
    select * from {{ ref('refunds') }}
),

renamed as (
    select
        cast(refund_id as integer) as refund_id,
        cast(payment_id as integer) as payment_id,
        cast(order_id as integer) as order_id,
        cast(refund_date as date) as refund_date,
        cast(amount as double) as amount,
        cast(reason as varchar) as reason
    from source
)

select * from renamed
