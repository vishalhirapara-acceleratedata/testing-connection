with order_items as (
    select * from {{ ref('stg_ecommerce__order_items') }}
),

products as (
    select * from {{ ref('stg_ecommerce__products') }}
),

orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),

enriched as (
    select
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        oi.quantity,
        oi.unit_price,
        oi.discount_amount,
        oi.quantity * oi.unit_price - oi.discount_amount as line_total,
        p.name as product_name,
        p.category_id,
        p.cost as product_cost,
        o.customer_id,
        o.order_date,
        o.status as order_status
    from order_items oi
    inner join products p on oi.product_id = p.product_id
    inner join orders o on oi.order_id = o.order_id
)

select * from enriched
