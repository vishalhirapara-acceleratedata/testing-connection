with source as (
    select * from {{ ref('inventory') }}
),

renamed as (
    select
        cast(inventory_id as integer) as inventory_id,
        cast(product_id as integer) as product_id,
        cast(warehouse_id as integer) as warehouse_id,
        cast(quantity as integer) as quantity,
        cast(last_updated as timestamp) as last_updated
    from source
)

select * from renamed
