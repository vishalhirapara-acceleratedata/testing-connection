{{
    config(
        materialized='table'
    )
}}

-- Customer dimension with control columns
with customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        customer_id,
        company_name,
        industry,
        country,
        created_date,
        is_active,
        -- Mandatory control columns
        current_timestamp as _loaded_at,
        '{{ invocation_id }}' as _dbt_invocation_id
    from customers
)

select * from final
