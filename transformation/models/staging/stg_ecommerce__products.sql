with source as (
    select * from {{ ref('products') }}
),

renamed as (
    select
        cast(product_id as integer) as product_id,
        cast(name as varchar) as name,
        cast(description as varchar) as description,
        cast(price as double) as price,
        cast(cost as double) as cost,
        cast(category_id as integer) as category_id,
        cast(created_at as timestamp) as created_at,
        cast(is_active as boolean) as is_active
    from source
)

select * from renamed
