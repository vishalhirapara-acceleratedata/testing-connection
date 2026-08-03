with customer_orders as (
    select * from {{ ref('int_customer_orders') }}
),

addresses as (
    select * from {{ ref('stg_ecommerce__addresses') }}
    where address_type = 'shipping'
),

customer_segments as (
    select * from {{ ref('stg_ecommerce__customer_segments') }}
),

primary_address as (
    select
        customer_id,
        city as address_city,
        state as address_state,
        country as address_country
    from addresses
    qualify row_number() over (partition by customer_id order by address_id) = 1
),

latest_segment as (
    select
        customer_id,
        segment_name
    from customer_segments
    qualify row_number() over (partition by customer_id order by assigned_at desc) = 1
)

select
    {{ dbt_utils.generate_surrogate_key(['co.customer_id']) }} as customer_key,
    co.customer_id,
    co.first_name,
    co.last_name,
    co.email,
    co.phone,
    co.total_orders,
    co.total_spent,
    co.first_order_date,
    co.last_order_date,
    co.avg_order_value,
    ls.segment_name,
    pa.address_city,
    pa.address_state,
    pa.address_country,
    co.created_at
from customer_orders co
left join primary_address pa on co.customer_id = pa.customer_id
left join latest_segment ls on co.customer_id = ls.customer_id
