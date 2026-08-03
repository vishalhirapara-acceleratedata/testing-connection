with source as (
    select * from {{ ref('order_status_history') }}
),

renamed as (
    select
        cast(status_id as integer) as status_id,
        cast(order_id as integer) as order_id,
        cast(status as varchar) as status,
        cast(changed_at as timestamp) as changed_at,
        cast(changed_by as varchar) as changed_by
    from source
)

select * from renamed
