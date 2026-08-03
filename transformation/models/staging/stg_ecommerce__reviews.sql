with source as (
    select * from {{ ref('reviews') }}
),

renamed as (
    select
        cast(review_id as integer) as review_id,
        cast(product_id as integer) as product_id,
        cast(customer_id as integer) as customer_id,
        cast(rating as integer) as rating,
        cast(comment as varchar) as comment,
        cast(created_at as date) as created_at
    from source
)

select * from renamed
