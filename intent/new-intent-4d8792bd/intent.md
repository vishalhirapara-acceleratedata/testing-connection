# Intent: Salesdata Mart Pipeline

## Goal
Build an end-to-end sales data pipeline on DuckDB-local: land raw JSON sales data into a bronze layer via a dlt ingestion pipeline, then transform it into a clean salesdata mart using dbt (staging → mart). The mart should serve analytical queries on orders, revenue, and customers.

## Source system
JSON flat files containing raw sales data (orders, customers, products). Synthetic seed JSON files will be generated if no source files exist yet.

## Target
DuckDB (local) — ephemeral sandbox at `$VD_EPHM_DUCKDB_PATH`. Schema: `main`.

## Objects in scope
- Raw JSON files: orders, customers, products
- Bronze DuckDB tables (landed by dlt)
- dbt staging models (stg_orders, stg_customers, stg_products)
- dbt mart models (fct_orders, dim_customers, dim_products)

## Deliverables inventory

| # | Deliverable | Kind | Notes |
| --- | --- | --- | --- |
| 1 | Sales JSON ingestion pipeline | pipeline | dlt pipeline landing JSON files into DuckDB bronze tables |
| 2 | Salesdata mart | mart/model | dbt staging + mart layer (fct_orders, dim_customers, dim_products) |

## Success criteria
- dlt pipeline loads all three JSON source files into bronze DuckDB with correct row counts
- `dbt build` compiles and runs clean (no errors) against the ephemeral DuckDB
- `dbt test` passes all not-null and unique tests on primary keys
- `fct_orders` grain: one row per order; `dim_customers` grain: one row per customer; `dim_products` grain: one row per product

## Out of scope
- Production / domain DuckDB writes (ephemeral sandbox only)
- Scheduling / orchestration
- Semantic model / BI layer
- Real external SaaS connectors

## Open questions
- None — source confirmed as JSON flat files

## Classification
- `action` = work
- `type` = mixed (ingestion + transformation)
- `scale` = product

## Approvals

The coordinator flips this only after a successful `AskUserQuestion` response of `approved`. Do not check by inference. Design, ship, and breaking-schema-delta approvals consolidate in `design.md`.

- [x] User approved intent — `2026-07-29 08:51` (UTC)
