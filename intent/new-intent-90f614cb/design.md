# Design: E-Commerce dbt Models — 20-Table Star Schema

## Architecture

**Platform:** DuckDB-local (`VD_DOMAIN_DATA_PLATFORM=duckdb`). All models run in the ephemeral DuckDB sandbox resolved from `$VD_EPHM_DUCKDB_PATH`.

**Source loading:** 20 CSV files placed in `seeds/ecommerce/` and loaded via dbt seeds. Each seed maps 1:1 to a staging model.

**Medallion layers:**
- **Staging** — views, 1:1 with source CSVs, clean column names (snake_case), basic type casting, no business logic
- **Intermediate** — views, enrichment joins and aggregations that feed multiple marts
- **Marts** — tables, star schema with surrogate keys, business logic, conformed dimensions

**Key decisions:**
- Surrogate keys via `dbt_utils.generate_surrogate_key()` for all dimension and fact tables
- Seeds over external tables for portability — CSV files are small sample data
- Staging models are views (zero cost, pass-through); marts are tables (materialized for query performance)
- All timestamps stored as `timestamp` type; dates as `date` type
- Soft deletes filtered in staging (`is_deleted = false` where applicable)

## Model Inventory

| # | Model | Layer | Materialization | Grain / Purpose | Depends on |
|---|-------|-------|-----------------|-----------------|------------|
| 1 | stg_ecommerce__customers | staging | view | One row per customer | seed_customers |
| 2 | stg_ecommerce__addresses | staging | view | One row per address | seed_addresses |
| 3 | stg_ecommerce__products | staging | view | One row per product | seed_products |
| 4 | stg_ecommerce__categories | staging | view | One row per category | seed_categories |
| 5 | stg_ecommerce__product_categories | staging | view | One row per product-category link | seed_product_categories |
| 6 | stg_ecommerce__orders | staging | view | One row per order | seed_orders |
| 7 | stg_ecommerce__order_items | staging | view | One row per line item | seed_order_items |
| 8 | stg_ecommerce__payments | staging | view | One row per payment | seed_payments |
| 9 | stg_ecommerce__refunds | staging | view | One row per refund | seed_refunds |
| 10 | stg_ecommerce__shipments | staging | view | One row per shipment | seed_shipments |
| 11 | stg_ecommerce__inventory | staging | view | One row per product-warehouse stock record | seed_inventory |
| 12 | stg_ecommerce__suppliers | staging | view | One row per supplier | seed_suppliers |
| 13 | stg_ecommerce__reviews | staging | view | One row per review | seed_reviews |
| 14 | stg_ecommerce__coupons | staging | view | One row per coupon definition | seed_coupons |
| 15 | stg_ecommerce__order_coupons | staging | view | One row per coupon usage | seed_order_coupons |
| 16 | stg_ecommerce__warehouses | staging | view | One row per warehouse | seed_warehouses |
| 17 | stg_ecommerce__returns | staging | view | One row per return | seed_returns |
| 18 | stg_ecommerce__customer_segments | staging | view | One row per segment assignment | seed_customer_segments |
| 19 | stg_ecommerce__product_suppliers | staging | view | One row per product-supplier link | seed_product_suppliers |
| 20 | stg_ecommerce__order_status_history | staging | view | One row per status change | seed_order_status_history |
| 21 | int_order_items_enriched | intermediate | view | One row per line item with product + order context | stg_order_items, stg_products, stg_orders |
| 22 | int_customer_orders | intermediate | view | One row per customer with order aggregates | stg_customers, stg_orders, stg_payments |
| 23 | dim_customer | mart | table | One row per customer | int_customer_orders, stg_addresses, stg_customer_segments |
| 24 | dim_product | mart | table | One row per product | stg_products, stg_categories, stg_product_categories, stg_suppliers, stg_product_suppliers |
| 25 | fct_orders | mart | table | One row per order | stg_orders, stg_payments, stg_shipments, stg_coupons, stg_order_coupons |
| 26 | fct_order_items | mart | table | One row per order line item | int_order_items_enriched, stg_refunds, stg_returns |
| 27 | fct_inventory_daily | mart | table | One row per product per warehouse per day | stg_inventory, stg_warehouses, stg_products |

## Source Mapping / Discovery

| Source CSV | Columns | Row count (sample) | Staging model |
|------------|---------|-------------------|---------------|
| customers.csv | customer_id, first_name, last_name, email, phone, created_at, is_deleted | 50 | stg_ecommerce__customers |
| addresses.csv | address_id, customer_id, address_type, street, city, state, postal_code, country | 80 | stg_ecommerce__addresses |
| products.csv | product_id, name, description, price, cost, category_id, created_at, is_active | 30 | stg_ecommerce__products |
| categories.csv | category_id, name, parent_category_id | 8 | stg_ecommerce__categories |
| product_categories.csv | product_id, category_id | 40 | stg_ecommerce__product_categories |
| orders.csv | order_id, customer_id, order_date, status, total_amount, shipping_address_id | 100 | stg_ecommerce__orders |
| order_items.csv | order_item_id, order_id, product_id, quantity, unit_price, discount_amount | 200 | stg_ecommerce__order_items |
| payments.csv | payment_id, order_id, payment_date, amount, method, status | 120 | stg_ecommerce__payments |
| refunds.csv | refund_id, payment_id, order_id, refund_date, amount, reason | 15 | stg_ecommerce__refunds |
| shipments.csv | shipment_id, order_id, carrier, tracking_number, shipped_date, delivered_date, status | 90 | stg_ecommerce__shipments |
| inventory.csv | inventory_id, product_id, warehouse_id, quantity, last_updated | 60 | stg_ecommerce__inventory |
| suppliers.csv | supplier_id, name, contact_email, phone, country | 10 | stg_ecommerce__suppliers |
| reviews.csv | review_id, product_id, customer_id, rating, comment, created_at | 40 | stg_ecommerce__reviews |
| coupons.csv | coupon_id, code, discount_type, discount_value, min_order_amount, expires_at | 10 | stg_ecommerce__coupons |
| order_coupons.csv | order_coupon_id, order_id, coupon_id, discount_amount | 20 | stg_ecommerce__order_coupons |
| warehouses.csv | warehouse_id, name, city, country | 4 | stg_ecommerce__warehouses |
| returns.csv | return_id, order_id, order_item_id, return_date, reason, status, refund_amount | 10 | stg_ecommerce__returns |
| customer_segments.csv | segment_id, customer_id, segment_name, assigned_at | 50 | stg_ecommerce__customer_segments |
| product_suppliers.csv | product_supplier_id, product_id, supplier_id, supply_price, lead_time_days | 35 | stg_ecommerce__product_suppliers |
| order_status_history.csv | status_id, order_id, status, changed_at, changed_by | 150 | stg_ecommerce__order_status_history |

## Change Impact

**No impact.** This is a greenfield build — no existing models, no downstream consumers. All 27 models are new. No breaking schema changes possible since nothing exists yet.

## Approvals
- [x] User approved design — 2026-08-03 06:55 (UTC)
