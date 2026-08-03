with source as (
    select * from {{ ref('returns') }}
),

renamed as (
    select
        cast(return_id as integer) as return_id,
        cast(order_id as integer) as order_id,
        cast(order_item_id as integer) as order_item_id,
        cast(return_date as date) as return_date,
        cast(reason as varchar) as reason,
        cast(status as varchar) as status,
        cast(refund_amount as double) as refund_amount
    from source
)

select * from renamed
