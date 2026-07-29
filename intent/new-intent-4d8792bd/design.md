# Design: Salesdata Mart Pipeline

## Architecture

**Platform:** DuckDB-local (`VD_DOMAIN_DATA_PLATFORM=duckdb`).  
**Sandbox:** `$VD_EPHM_DUCKDB_PATH` — all writes target the ephemeral DuckDB; domain DuckDB is read-only.

**Ingestion layer (dlt):**  
A dlt pipeline reads three local JSON flat files (orders, customers, products) via custom `@dlt.resource` decorated functions and lands them into bronze tables in the ephemeral DuckDB (`schema=main`). Synthetic seed JSON files will be generated if source files do not exist. Write disposition: `replace` (full load, no cursor needed). Schema contract: `columns=freeze`, `tables=evolve` (pinned to `freeze` post-first-load), `data_type=freeze`.

**Transformation layer (dbt):**  
A dbt project reads the bronze tables as sources and transforms them through two layers:
- **Staging** (`view`): 1:1 rename/cast of each bronze table — `stg_salesdata__orders`, `stg_salesdata__customers`, `stg_salesdata__products`.
- **Mart** (`table`): `fct_orders` (grain: one row per order), `dim_customers` (grain: one row per customer), `dim_products` (grain: one row per product).

dbt profile targets the ephemeral DuckDB path via `$VD_EPHM_DUCKDB_PATH`. No intermediate layer needed (joins are simple; business logic is thin). No schedule or semantic model in scope.

**Key decisions:**
- `replace` disposition for JSON flat files — no incrementality needed; files are small and fully re-loaded each run.
- No intermediate models — grain commitment goes directly from staging; logic is projection-only.
- Ephemeral sandbox only — domain DuckDB is never written to.

## Pipeline Inventory

| resource | entry_point | columns | tables | data_type | write_disposition | incremental_cursor | notes | status |
|----------|-------------|---------|--------|-----------|-------------------|--------------------|-------|--------|
| orders | orders | freeze | evolve | freeze | replace | | primary_key=order_id | working |
| customers | customers | freeze | evolve | freeze | replace | | primary_key=customer_id | working |
| products | products | freeze | evolve | freeze | replace | | primary_key=product_id | working |

## Model Inventory

| model | layer | grain | materialization | source | status |
|-------|-------|-------|-----------------|--------|--------|
| stg_salesdata__orders | staging | one row per order | view | bronze orders table | working |
| stg_salesdata__customers | staging | one row per customer | view | bronze customers table | working |
| stg_salesdata__products | staging | one row per product | view | bronze products table | working |
| fct_orders | mart | one row per order | table | stg_salesdata__orders + stg_salesdata__customers + stg_salesdata__products | working |
| dim_customers | mart | one row per customer | table | stg_salesdata__customers | working |
| dim_products | mart | one row per product | table | stg_salesdata__products | working |

## Source Mapping / Discovery

**Ingestion source:** Local JSON flat files (not a dlt verified-source connector; no `.dlt/config.toml` registration required).  
Schema is defined from expected sales-data conventions:

| File | Bronze table | Key columns |
|------|-------------|-------------|
| `data/orders.json` | `main.orders` | order_id (PK), customer_id (FK), product_id (FK), order_date, quantity, unit_price, total_amount, status |
| `data/customers.json` | `main.customers` | customer_id (PK), customer_name, email, city, country, created_at |
| `data/products.json` | `main.products` | product_id (PK), product_name, category, unit_price, created_at |

Synthetic seed files will be generated at `data/` by `generating-dlt-pipeline` if not present.

**Transformation source:** bronze tables in ephemeral DuckDB registered as dbt sources under `salesdata` source block.

## Change Impact

Fresh build — no existing models, contracts, or downstream consumers. No impact.

## Build Plan

- `01-generate-dlt-pipeline` — phase: Build — goal: Generate synthetic JSON seed files at `data/` and dlt pipeline `ingestion/salesdata_pipeline.py` with `@dlt.resource` functions for orders, customers, products; DuckDB destination wired to `$VD_EPHM_DUCKDB_PATH` — skill: `generating-dlt-pipeline` — status: working — evidence:
- `02-run-dlt-sandbox` — phase: Build — goal: Run dlt pipeline against ephemeral DuckDB; confirm bronze tables land with correct row counts — skill: `running-dlt-in-sandbox` — status: working — evidence:
- `03-bronze-preview` — phase: Build — goal: Render bronze preview to `ingestion/last-run-preview.md` from landed tables — skill: `running-dlt-in-sandbox` (bronze-preview step) — status: working — evidence:
- `04-scaffold-dbt-project` — phase: Build — goal: Scaffold dbt project at `transformation/` (`dbt_project.yml`, `profiles.yml` targeting `$VD_EPHM_DUCKDB_PATH`, `packages.yml`) — skill: `generating-dbt-model` — status: working — evidence:
- `05-generate-dbt-staging` — phase: Build — goal: Generate `sources.yml` + staging models `stg_salesdata__orders`, `stg_salesdata__customers`, `stg_salesdata__products` with schema YAML and not-null/unique tests — skill: `generating-dbt-model` — status: working — evidence:
- `06-generate-dbt-mart` — phase: Build — goal: Generate mart models `fct_orders`, `dim_customers`, `dim_products` with schema YAML, not-null/unique tests — skill: `generating-dbt-model` — status: working — evidence:
- `07-run-dbt-sandbox` — phase: Build — goal: `dbt build` against ephemeral DuckDB; all models compile and materialize; all tests pass — skill: `running-dbt-in-sandbox` — status: working — evidence:
- `08-dlt-unit-tests` — phase: Build — goal: pytest unit tests for dlt resource functions (row shape, schema contract, no-live-file) — skill: `dlt-unit-testing` — status: working — evidence:
- `09-dbt-unit-tests` — phase: Build — goal: dbt unit tests for staging casts and mart grain — skill: `dbt-unit-testing` — status: working — evidence:
- `10-ingestion-data-tests` — phase: Verify — goal: Bronze row-count, null-rate, freshness, and key-quality checks on landed tables — skill: `ingestion-data-testing` — status: working — evidence:
- `11-evaluate-dlt-pipeline` — phase: Verify — goal: Audit dlt pipeline against invariants (entry_point, schema_contract, naming, disposition) — skill: `evaluating-dlt-pipeline` — status: working — evidence:
- `12-evaluate-dbt-project` — phase: Verify — goal: `dbt_project_evaluator` + convention compliance audit — skill: `evaluating-dbt-project` — status: working — evidence:
- `13-register-dbt-sources` — phase: Publish — goal: Register bronze tables as dbt sources in `transformation/models/sources.yml` — skill: `registering-dbt-sources` — status: working — evidence:
- `14-publish-dbt-contracts` — phase: Publish — goal: Enforce dbt contracts on mart models; publish docs — skill: `publishing-dbt-contracts` — status: working — evidence:
- `15-verifying-completion-claims` — phase: Publish — goal: Deterministic backstop — confirm all steps done, all evidence recorded — skill: `verifying-completion-claims` — status: working — evidence:

## Gate Ledger

- ✅ Intent gate — approved 2026-07-29 08:51 UTC
- ⬜ Design gate
- ⬜ Build gate
- ⬜ Verify gate
- ⬜ Publish gate

## Approvals

The coordinator flips these only after a successful `AskUserQuestion` response of `approved`. Do not check by inference.

- [x] User approved intent — `2026-07-29 08:51` (UTC)
- [ ] User approved design — `YYYY-MM-DD HH:MM` (UTC)
- [ ] User approved ship — `YYYY-MM-DD HH:MM` (UTC)
- [ ] User approved breaking schema delta — N/A
