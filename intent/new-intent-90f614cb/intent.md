---
kind: transformation
express: true
---

# Intent: E-Commerce dbt Models — 20-Table Star Schema

## Goal
Build a complete dbt transformation layer for an e-commerce business with 20 source tables, producing a star schema of dimensions and facts that enables customer analytics, order analytics, product analytics, and inventory tracking.

## Source system
20 CSV files representing e-commerce operational data: customers, addresses, products, categories, product_categories, orders, order_items, payments, refunds, shipments, inventory, suppliers, reviews, coupons, order_coupons, warehouses, returns, customer_segments, product_suppliers, order_status_history.

## Target
DuckDB-local dbt project with staging (views), intermediate (views), and mart (tables) layers.

## Objects in scope
- 20 staging models (`stg_ecommerce__<table>`)
- 2 intermediate models (`int_order_items_enriched`, `int_customer_orders`)
- 5 mart models (`dim_customer`, `dim_product`, `fct_orders`, `fct_order_items`, `fct_inventory_daily`)
- Sample CSV data for all 20 source tables

## Deliverables inventory

| # | Deliverable | Kind | Notes |
|---|-------------|------|-------|
| 1 | 20 source CSV files | source data | Sample e-commerce data with realistic relationships |
| 2 | 20 staging models | mart/model | Views, one per source table, clean column names |
| 3 | 2 intermediate models | mart/model | Enriched order items, customer order aggregates |
| 4 | dim_customer | mart/model | Grain: one row per customer |
| 5 | dim_product | mart/model | Grain: one row per product |
| 6 | fct_orders | mart/model | Grain: one row per order |
| 7 | fct_order_items | mart/model | Grain: one row per order line item |
| 8 | fct_inventory_daily | mart/model | Grain: one row per product per warehouse per day |

## Success criteria
- All 20 staging models compile and pass schema tests
- All 5 mart models produce correct output against sample data
- Primary keys are unique and not null on all marts
- Foreign key relationships are valid
- `dbt build` exits 0 in the DuckDB sandbox

## Out of scope
- Orchestration / scheduling (separate intent if needed)
- Semantic model / metrics layer (separate intent if needed)
- Data ingestion pipeline (CSV files are the source, loaded directly)
- Production deployment to a remote warehouse

## Open questions
- None

## Approvals
- [x] User approved intent — 2026-08-03 06:54 (UTC)
