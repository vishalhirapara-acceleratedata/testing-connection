with source as (
    select * from {{ ref('product_categories') }}
),

renamed as (
    select
        cast(product_id as integer) as product_id,
        cast(category_id as integer) as category_id
    from source
)

select * from renamed
