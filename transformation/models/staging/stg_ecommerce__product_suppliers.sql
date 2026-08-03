with source as (
    select * from {{ ref('product_suppliers') }}
),

renamed as (
    select
        cast(product_supplier_id as integer) as product_supplier_id,
        cast(product_id as integer) as product_id,
        cast(supplier_id as integer) as supplier_id,
        cast(supply_price as double) as supply_price,
        cast(lead_time_days as integer) as lead_time_days
    from source
)

select * from renamed
