with source as (
    select * from {{ ref('customers') }}
),

renamed as (
    select
        cast(customer_id as integer) as customer_id,
        cast(first_name as varchar) as first_name,
        cast(last_name as varchar) as last_name,
        cast(email as varchar) as email,
        cast(phone as varchar) as phone,
        cast(created_at as timestamp) as created_at,
        cast(is_deleted as boolean) as is_deleted
    from source
)

select * from renamed
