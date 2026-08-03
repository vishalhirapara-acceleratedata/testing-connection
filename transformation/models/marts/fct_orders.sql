with orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),

payments as (
    select
        order_id,
        sum(amount) as payment_amount
    from {{ ref('stg_ecommerce__payments') }}
    where status = 'completed'
    group by order_id
),

refunds as (
    select
        order_id,
        sum(amount) as refund_amount
    from {{ ref('stg_ecommerce__refunds') }}
    group by order_id
),

shipments as (
    select
        order_id,
        status as shipping_status
    from {{ ref('stg_ecommerce__shipments') }}
    qualify row_number() over (partition by order_id order by shipped_date desc) = 1
),

order_coupons as (
    select
        oc.order_id,
        max(c.code) as coupon_code,
        sum(oc.discount_amount) as coupon_discount
    from {{ ref('stg_ecommerce__order_coupons') }} oc
    left join {{ ref('stg_ecommerce__coupons') }} c on oc.coupon_id = c.coupon_id
    group by oc.order_id
),

returns as (
    select distinct
        order_id,
        true as is_returned
    from {{ ref('stg_ecommerce__returns') }}
    where status = 'approved'
)

select
    {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} as order_key,
    o.order_id,
    {{ dbt_utils.generate_surrogate_key(['o.customer_id']) }} as customer_key,
    o.order_date,
    o.status,
    o.total_amount,
    coalesce(oc.coupon_discount, 0) as discount_amount,
    coalesce(pay.payment_amount, 0) as payment_amount,
    coalesce(ref.refund_amount, 0) as refund_amount,
    sh.shipping_status,
    oc.coupon_code,
    coalesce(ret.is_returned, false) as is_returned
from orders o
left join payments pay on o.order_id = pay.order_id
left join refunds ref on o.order_id = ref.order_id
left join shipments sh on o.order_id = sh.order_id
left join order_coupons oc on o.order_id = oc.order_id
left join returns ret on o.order_id = ret.order_id
