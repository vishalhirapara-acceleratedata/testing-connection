with source as (
    select * from {{ source('bronze', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        sales_rep_id,
        order_date,
        total_amount,
        status
    from source
)

select * from renamed
