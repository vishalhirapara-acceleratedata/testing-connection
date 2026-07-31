-- Staging model for customers
-- Grain: customer_id

with source as (
    select * from {{ source('bronze', 'customers') }}
),

renamed as (
    select
        customer_id,
        company_name,
        industry,
        country,
        created_date,
        is_active,
        -- dlt system columns
        _dlt_load_id,
        _dlt_id
    from source
)

select * from renamed
where is_active = true
