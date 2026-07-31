-- Staging model for products
with source as (
    select * from {{ source('bronze', 'products') }}
),

renamed as (
    select
        product_id,
        product_name,
        product_type,
        category_id,
        list_price,
        is_active
    from source
)

select * from renamed
where is_active = true
