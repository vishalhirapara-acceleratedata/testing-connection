with inventory as (
    select * from {{ ref('stg_ecommerce__inventory') }}
),

warehouses as (
    select * from {{ ref('stg_ecommerce__warehouses') }}
),

products as (
    select * from {{ ref('stg_ecommerce__products') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['inv.inventory_id']) }} as inventory_key,
    {{ dbt_utils.generate_surrogate_key(['inv.product_id']) }} as product_key,
    inv.warehouse_id,
    cast(inv.last_updated as date) as date,
    inv.quantity,
    p.name as product_name,
    w.name as warehouse_name
from inventory inv
left join warehouses w on inv.warehouse_id = w.warehouse_id
left join products p on inv.product_id = p.product_id
