with source as (
    select * from {{ ref('warehouses') }}
),

renamed as (
    select
        cast(warehouse_id as integer) as warehouse_id,
        cast(name as varchar) as name,
        cast(city as varchar) as city,
        cast(country as varchar) as country
    from source
)

select * from renamed
