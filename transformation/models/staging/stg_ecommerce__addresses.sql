with source as (
    select * from {{ ref('addresses') }}
),

renamed as (
    select
        cast(address_id as integer) as address_id,
        cast(customer_id as integer) as customer_id,
        cast(address_type as varchar) as address_type,
        cast(street as varchar) as street,
        cast(city as varchar) as city,
        cast(state as varchar) as state,
        cast(postal_code as varchar) as postal_code,
        cast(country as varchar) as country
    from source
)

select * from renamed
