# Plan: E-Commerce dbt Models — 20-Table Star Schema

`plan.md` is one of four durable artifacts, one per primitive, and it is the only one that carries progress — task checkboxes plus per-task `## Execution evidence`.

**Goal:** Build a complete dbt transformation layer with 20 staging models, 2 intermediate models, and 5 mart models from sample e-commerce CSV data, running on DuckDB-local.

**Architecture:** CSV seed files → staging views (1:1 cleaning) → intermediate views (enrichment) → mart tables (star schema). All models follow the naming conventions in AGENTS.md.

**Tech Stack:** dbt-core, dbt-duckdb, DuckDB

## Global Constraints

- Platform: DuckDB-local (`VD_DOMAIN_DATA_PLATFORM=duckdb`)
- Sandbox path: `$VD_EPHM_DUCKDB_PATH`
- Naming: staging `stg_ecommerce__<table>`, facts `fct_<process>`, dimensions `dim_<entity>`
- Materialization: staging/intermediate = views, marts = tables
- Primary keys: `not_null` + `unique` tests on all mart PKs
- dbt project root: `/workspace/transformation/`
- Seeds directory: `/workspace/transformation/seeds/ecommerce/`

---

## Tasks

### Task 1: Set up dbt project and create 20 seed CSV files

**Files:**
- Create: `transformation/dbt_project.yml`
- Create: `transformation/profiles.yml`
- Create: `transformation/seeds/ecommerce/customers.csv`
- Create: `transformation/seeds/ecommerce/addresses.csv`
- Create: `transformation/seeds/ecommerce/products.csv`
- Create: `transformation/seeds/ecommerce/categories.csv`
- Create: `transformation/seeds/ecommerce/product_categories.csv`
- Create: `transformation/seeds/ecommerce/orders.csv`
- Create: `transformation/seeds/ecommerce/order_items.csv`
- Create: `transformation/seeds/ecommerce/payments.csv`
- Create: `transformation/seeds/ecommerce/refunds.csv`
- Create: `transformation/seeds/ecommerce/shipments.csv`
- Create: `transformation/seeds/ecommerce/inventory.csv`
- Create: `transformation/seeds/ecommerce/suppliers.csv`
- Create: `transformation/seeds/ecommerce/reviews.csv`
- Create: `transformation/seeds/ecommerce/coupons.csv`
- Create: `transformation/seeds/ecommerce/order_coupons.csv`
- Create: `transformation/seeds/ecommerce/warehouses.csv`
- Create: `transformation/seeds/ecommerce/returns.csv`
- Create: `transformation/seeds/ecommerce/customer_segments.csv`
- Create: `transformation/seeds/ecommerce/product_suppliers.csv`
- Create: `transformation/seeds/ecommerce/order_status_history.csv`

**Interfaces:**
- Consumes: Nothing (first task)
- Produces: dbt project config, 20 seed CSV files with realistic e-commerce data

- [ ] **Step 1: Create dbt_project.yml**

```yaml
name: 'ecommerce'
version: '1.0.0'
config-version: 2
profile: 'ecommerce'
model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
target-path: "target"
clean-targets: ["target", "dbt_packages"]
seeds:
  ecommerce:
    +schema: raw
models:
  ecommerce:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

- [ ] **Step 2: Create profiles.yml**

```yaml
ecommerce:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: "{{ env_var('VD_EPHM_DUCKDB_PATH') }}"
      threads: 4
```

- [ ] **Step 3: Create all 20 seed CSV files with sample data**

Generate realistic e-commerce sample data with proper referential integrity:
- 50 customers, 80 addresses, 30 products, 8 categories
- 100 orders, 200 order items, 120 payments
- 15 refunds, 90 shipments, 60 inventory records
- 10 suppliers, 40 reviews, 10 coupons, 20 order_coupons
- 4 warehouses, 10 returns, 50 customer_segments
- 35 product_suppliers, 150 order_status_history

- [ ] **Step 4: Verify seeds load**

Run: `cd /workspace/transformation && dbt seed --profiles-dir .`
Expected: All 20 seeds loaded successfully

- [ ] **Step 5: Commit**

```bash
git add transformation/dbt_project.yml transformation/profiles.yml transformation/seeds/
git commit -m "feat: add dbt project setup and 20 e-commerce seed CSV files"
```

### Task 2: Generate 20 staging models

**Files:**
- Create: `transformation/models/staging/stg_ecommerce__customers.sql`
- Create: `transformation/models/staging/stg_ecommerce__addresses.sql`
- Create: `transformation/models/staging/stg_ecommerce__products.sql`
- Create: `transformation/models/staging/stg_ecommerce__categories.sql`
- Create: `transformation/models/staging/stg_ecommerce__product_categories.sql`
- Create: `transformation/models/staging/stg_ecommerce__orders.sql`
- Create: `transformation/models/staging/stg_ecommerce__order_items.sql`
- Create: `transformation/models/staging/stg_ecommerce__payments.sql`
- Create: `transformation/models/staging/stg_ecommerce__refunds.sql`
- Create: `transformation/models/staging/stg_ecommerce__shipments.sql`
- Create: `transformation/models/staging/stg_ecommerce__inventory.sql`
- Create: `transformation/models/staging/stg_ecommerce__suppliers.sql`
- Create: `transformation/models/staging/stg_ecommerce__reviews.sql`
- Create: `transformation/models/staging/stg_ecommerce__coupons.sql`
- Create: `transformation/models/staging/stg_ecommerce__order_coupons.sql`
- Create: `transformation/models/staging/stg_ecommerce__warehouses.sql`
- Create: `transformation/models/staging/stg_ecommerce__returns.sql`
- Create: `transformation/models/staging/stg_ecommerce__customer_segments.sql`
- Create: `transformation/models/staging/stg_ecommerce__product_suppliers.sql`
- Create: `transformation/models/staging/stg_ecommerce__order_status_history.sql`
- Create: `transformation/models/staging/schema.yml`

**Interfaces:**
- Consumes: 20 seed tables from Task 1
- Produces: 20 staging views + schema YAML with column descriptions

- [ ] **Step 1: Generate all 20 staging models**

Each staging model follows the pattern:
```sql
with source as (
    select * from {{ ref('seed_<table>') }}
),
renamed as (
    select
        -- column list with type casting
    from source
)
select * from renamed
```

- [ ] **Step 2: Create staging schema.yml**

Define sources and column tests for all 20 staging models.

- [ ] **Step 3: Run dbt build on staging models**

Run: `cd /workspace/transformation && dbt build --models staging/ --profiles-dir .`
Expected: 20 staging models built successfully

- [ ] **Step 4: Commit**

```bash
git add transformation/models/staging/
git commit -m "feat: add 20 staging models for e-commerce sources"
```

### Task 3: Generate 2 intermediate models

**Files:**
- Create: `transformation/models/intermediate/int_order_items_enriched.sql`
- Create: `transformation/models/intermediate/int_customer_orders.sql`
- Create: `transformation/models/intermediate/schema.yml`

**Interfaces:**
- Consumes: `stg_ecommerce__order_items`, `stg_ecommerce__products`, `stg_ecommerce__orders`, `stg_ecommerce__customers`, `stg_ecommerce__payments`
- Produces: `int_order_items_enriched` (line items with product + order context), `int_customer_orders` (customer-level aggregates)

- [ ] **Step 1: Generate int_order_items_enriched**

Join order_items with products and orders to enrich line items with product names, categories, order dates, and customer IDs.

- [ ] **Step 2: Generate int_customer_orders**

Aggregate customer order history: total orders, total spent, first/last order dates, average order value.

- [ ] **Step 3: Create intermediate schema.yml**

- [ ] **Step 4: Run dbt build on intermediate models**

Run: `cd /workspace/transformation && dbt build --models intermediate/ --profiles-dir .`
Expected: 2 intermediate models built successfully

- [ ] **Step 5: Commit**

```bash
git add transformation/models/intermediate/
git commit -m "feat: add intermediate models for order enrichment and customer aggregation"
```

### Task 4: Generate 5 mart models

**Files:**
- Create: `transformation/models/marts/dim_customer.sql`
- Create: `transformation/models/marts/dim_product.sql`
- Create: `transformation/models/marts/fct_orders.sql`
- Create: `transformation/models/marts/fct_order_items.sql`
- Create: `transformation/models/marts/fct_inventory_daily.sql`
- Create: `transformation/models/marts/schema.yml`

**Interfaces:**
- Consumes: All staging and intermediate models from Tasks 2-3
- Produces: 5 mart tables with primary key tests, foreign key relationships, and not_null constraints

- [ ] **Step 1: Generate dim_customer**

Grain: one row per customer. Columns: customer_key, customer_id, first_name, last_name, email, phone, total_orders, total_spent, first_order_date, last_order_date, segment_name, address_city, address_state, address_country, created_at.

- [ ] **Step 2: Generate dim_product**

Grain: one row per product. Columns: product_key, product_id, product_name, description, price, cost, category_name, supplier_name, is_active, created_at.

- [ ] **Step 3: Generate fct_orders**

Grain: one row per order. Columns: order_key, order_id, customer_key, order_date, status, total_amount, discount_amount, payment_amount, refund_amount, shipping_status, coupon_code, is_returned.

- [ ] **Step 4: Generate fct_order_items**

Grain: one row per order line item. Columns: order_item_key, order_item_id, order_key, product_key, order_date, quantity, unit_price, discount_amount, line_total, is_refunded, is_returned.

- [ ] **Step 5: Generate fct_inventory_daily**

Grain: one row per product per warehouse per day. Columns: inventory_key, product_key, warehouse_id, date, quantity, product_name, warehouse_name.

- [ ] **Step 6: Create marts schema.yml with tests**

Define primary key tests (unique + not_null), foreign key relationships, and accepted values for status columns.

- [ ] **Step 7: Run dbt build on all marts**

Run: `cd /workspace/transformation && dbt build --models marts/ --profiles-dir .`
Expected: 5 mart models built successfully, all tests pass

- [ ] **Step 8: Commit**

```bash
git add transformation/models/marts/
git commit -m "feat: add 5 mart models (dim_customer, dim_product, fct_orders, fct_order_items, fct_inventory_daily)"
```

### Task 5: Full dbt build and verification

**Files:**
- No new files

**Interfaces:**
- Consumes: All models from Tasks 1-4
- Produces: Verification that the full project builds and tests pass

- [ ] **Step 1: Run full dbt build**

Run: `cd /workspace/transformation && dbt build --profiles-dir .`
Expected: All 27 models built, all tests pass, exit code 0

- [ ] **Step 2: Verify model counts**

Run: `cd /workspace/transformation && dbt ls --profiles-dir . | wc -l`
Expected: 27 models listed

- [ ] **Step 3: Commit final state**

```bash
git add -A
git commit -m "chore: verify full dbt build passes for e-commerce project"
```

## Execution evidence

Append-only — one line per task, in task order.
