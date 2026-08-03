with products as (
    select * from {{ ref('stg_ecommerce__products') }}
),

categories as (
    select * from {{ ref('stg_ecommerce__categories') }}
),

product_suppliers as (
    select * from {{ ref('stg_ecommerce__product_suppliers') }}
),

suppliers as (
    select * from {{ ref('stg_ecommerce__suppliers') }}
),

primary_supplier as (
    select
        product_id,
        supplier_id
    from product_suppliers
    qualify row_number() over (partition by product_id order by product_supplier_id) = 1
)

select
    {{ dbt_utils.generate_surrogate_key(['p.product_id']) }} as product_key,
    p.product_id,
    p.name as product_name,
    p.description,
    p.price,
    p.cost,
    c.name as category_name,
    s.name as supplier_name,
    p.is_active,
    p.created_at
from products p
left join categories c on p.category_id = c.category_id
left join primary_supplier ps on p.product_id = ps.product_id
left join suppliers s on ps.supplier_id = s.supplier_id
