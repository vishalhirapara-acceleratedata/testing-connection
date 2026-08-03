with source as (
    select * from {{ ref('categories') }}
),

renamed as (
    select
        cast(category_id as integer) as category_id,
        cast(name as varchar) as name,
        cast(parent_category_id as integer) as parent_category_id
    from source
)

select * from renamed
