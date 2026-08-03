with customers as (
    select * from {{ ref('stg_ecommerce__customers') }}
),

orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),

payments as (
    select * from {{ ref('stg_ecommerce__payments') }}
    where status = 'completed'
),

customer_order_summary as (
    select
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.phone,
        c.created_at,
        c.is_deleted,
        count(distinct o.order_id) as total_orders,
        coalesce(sum(o.total_amount), 0) as total_spent,
        min(o.order_date) as first_order_date,
        max(o.order_date) as last_order_date,
        case
            when count(distinct o.order_id) > 0 then round(sum(o.total_amount) / count(distinct o.order_id), 2)
            else 0
        end as avg_order_value,
        coalesce(sum(pay.amount), 0) as total_paid
    from customers c
    left join orders o on c.customer_id = o.customer_id
    left join payments pay on o.order_id = pay.order_id
    group by all
)

select * from customer_order_summary
