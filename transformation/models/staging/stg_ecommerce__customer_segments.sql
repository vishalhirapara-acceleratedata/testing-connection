with source as (
    select * from {{ ref('customer_segments') }}
),

renamed as (
    select
        cast(segment_id as integer) as segment_id,
        cast(customer_id as integer) as customer_id,
        cast(segment_name as varchar) as segment_name,
        cast(assigned_at as date) as assigned_at
    from source
)

select * from renamed
