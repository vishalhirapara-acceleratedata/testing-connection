with source as (
    select * from {{ ref('shipments') }}
),

renamed as (
    select
        cast(shipment_id as integer) as shipment_id,
        cast(order_id as integer) as order_id,
        cast(carrier as varchar) as carrier,
        cast(tracking_number as varchar) as tracking_number,
        cast(shipped_date as date) as shipped_date,
        cast(delivered_date as date) as delivered_date,
        cast(status as varchar) as status
    from source
)

select * from renamed
