with source as (
    select * from {{ ref('suppliers') }}
),

renamed as (
    select
        cast(supplier_id as integer) as supplier_id,
        cast(name as varchar) as name,
        cast(contact_email as varchar) as contact_email,
        cast(phone as varchar) as phone,
        cast(country as varchar) as country
    from source
)

select * from renamed
