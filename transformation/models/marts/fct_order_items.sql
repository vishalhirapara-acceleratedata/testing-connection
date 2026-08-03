with order_items_enriched as (
    select * from {{ ref('int_order_items_enriched') }}
),

refunds as (
    select distinct
        order_id
    from {{ ref('stg_ecommerce__refunds') }}
),

returns as (
    select distinct
        order_item_id
    from {{ ref('stg_ecommerce__returns') }}
    where status = 'approved'
)

select
    {{ dbt_utils.generate_surrogate_key(['oi.order_item_id']) }} as order_item_key,
    oi.order_item_id,
    {{ dbt_utils.generate_surrogate_key(['oi.order_id']) }} as order_key,
    {{ dbt_utils.generate_surrogate_key(['oi.product_id']) }} as product_key,
    oi.order_date,
    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    oi.line_total,
    case when ref.order_id is not null then true else false end as is_refunded,
    coalesce(ret.order_item_id is not null, false) as is_returned
from order_items_enriched oi
left join refunds ref on oi.order_id = ref.order_id
left join returns ret on oi.order_item_id = ret.order_item_id
