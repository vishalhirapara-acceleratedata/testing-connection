#!/usr/bin/env python3
"""dlt ingestion pipeline for IT business sales data."""

import os
import dlt
from pathlib import Path

# Get DuckDB path from environment
DUCKDB_PATH = os.getenv('VD_EPHM_DUCKDB_PATH')
if not DUCKDB_PATH:
    raise ValueError("VD_EPHM_DUCKDB_PATH environment variable not set")

# Ensure the parent directory exists
Path(DUCKDB_PATH).parent.mkdir(parents=True, exist_ok=True)

# CSV source data directory
SOURCE_DATA_DIR = Path(__file__).parent / 'sample_data'

# Table names (20 tables)
TABLES = [
    'territories',
    'channels',
    'sales_reps',
    'customers',
    'contacts',
    'customer_addresses',
    'customer_segments',
    'product_categories',
    'products',
    'licenses',
    'pricing_tiers',
    'opportunities',
    'quotes',
    'orders',
    'order_lines',
    'invoices',
    'invoice_lines',
    'payments',
    'support_tickets',
    'ticket_resolutions'
]


@dlt.resource(name='territories', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_territories():
    """Load territories from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'territories.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cast types
            row['territory_id'] = int(row['territory_id'])
            yield row


@dlt.resource(name='channels', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_channels():
    """Load channels from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'channels.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['channel_id'] = int(row['channel_id'])
            row['commission_rate'] = float(row['commission_rate'])
            yield row


@dlt.resource(name='sales_reps', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_sales_reps():
    """Load sales_reps from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'sales_reps.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['sales_rep_id'] = int(row['sales_rep_id'])
            row['territory_id'] = int(row['territory_id'])
            yield row


@dlt.resource(name='customers', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_customers():
    """Load customers from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'customers.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['customer_id'] = int(row['customer_id'])
            row['is_active'] = row['is_active'].lower() == 'true'
            yield row


@dlt.resource(name='contacts', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_contacts():
    """Load contacts from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'contacts.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['contact_id'] = int(row['contact_id'])
            row['customer_id'] = int(row['customer_id'])
            yield row


@dlt.resource(name='customer_addresses', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_customer_addresses():
    """Load customer_addresses from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'customer_addresses.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['address_id'] = int(row['address_id'])
            row['customer_id'] = int(row['customer_id'])
            yield row


@dlt.resource(name='customer_segments', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_customer_segments():
    """Load customer_segments from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'customer_segments.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['segment_id'] = int(row['segment_id'])
            row['customer_id'] = int(row['customer_id'])
            yield row


@dlt.resource(name='product_categories', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_product_categories():
    """Load product_categories from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'product_categories.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['category_id'] = int(row['category_id'])
            if row['parent_category_id']:
                row['parent_category_id'] = int(row['parent_category_id']) if row['parent_category_id'] != '' else None
            else:
                row['parent_category_id'] = None
            yield row


@dlt.resource(name='products', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_products():
    """Load products from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'products.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['product_id'] = int(row['product_id'])
            row['category_id'] = int(row['category_id'])
            row['list_price'] = float(row['list_price'])
            row['is_active'] = row['is_active'].lower() == 'true'
            yield row


@dlt.resource(name='licenses', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_licenses():
    """Load licenses from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'licenses.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['license_id'] = int(row['license_id'])
            row['product_id'] = int(row['product_id'])
            row['duration_months'] = int(row['duration_months']) if row['duration_months'] else None
            row['max_users'] = int(row['max_users']) if row['max_users'] else None
            yield row


@dlt.resource(name='pricing_tiers', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_pricing_tiers():
    """Load pricing_tiers from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'pricing_tiers.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['tier_id'] = int(row['tier_id'])
            row['product_id'] = int(row['product_id'])
            row['min_quantity'] = int(row['min_quantity'])
            row['max_quantity'] = int(row['max_quantity'])
            row['unit_price'] = float(row['unit_price'])
            yield row


@dlt.resource(name='opportunities', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_opportunities():
    """Load opportunities from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'opportunities.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['opportunity_id'] = int(row['opportunity_id'])
            row['customer_id'] = int(row['customer_id'])
            row['sales_rep_id'] = int(row['sales_rep_id'])
            row['value'] = float(row['value'])
            row['probability'] = float(row['probability'])
            yield row


@dlt.resource(name='quotes', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_quotes():
    """Load quotes from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'quotes.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['quote_id'] = int(row['quote_id'])
            row['opportunity_id'] = int(row['opportunity_id'])
            row['total_amount'] = float(row['total_amount'])
            yield row


@dlt.resource(name='orders', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_orders():
    """Load orders from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'orders.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['order_id'] = int(row['order_id'])
            row['customer_id'] = int(row['customer_id'])
            row['sales_rep_id'] = int(row['sales_rep_id'])
            row['total_amount'] = float(row['total_amount'])
            yield row


@dlt.resource(name='order_lines', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_order_lines():
    """Load order_lines from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'order_lines.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['order_line_id'] = int(row['order_line_id'])
            row['order_id'] = int(row['order_id'])
            row['line_number'] = int(row['line_number'])
            row['product_id'] = int(row['product_id'])
            row['quantity'] = int(row['quantity'])
            row['unit_price'] = float(row['unit_price'])
            row['line_total'] = float(row['line_total'])
            yield row


@dlt.resource(name='invoices', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_invoices():
    """Load invoices from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'invoices.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['invoice_id'] = int(row['invoice_id'])
            row['order_id'] = int(row['order_id'])
            row['total_amount'] = float(row['total_amount'])
            yield row


@dlt.resource(name='invoice_lines', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_invoice_lines():
    """Load invoice_lines from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'invoice_lines.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['invoice_line_id'] = int(row['invoice_line_id'])
            row['invoice_id'] = int(row['invoice_id'])
            row['line_number'] = int(row['line_number'])
            row['product_id'] = int(row['product_id'])
            row['quantity'] = int(row['quantity'])
            row['unit_price'] = float(row['unit_price'])
            row['line_total'] = float(row['line_total'])
            yield row


@dlt.resource(name='payments', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_payments():
    """Load payments from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'payments.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['payment_id'] = int(row['payment_id'])
            row['invoice_id'] = int(row['invoice_id'])
            row['amount'] = float(row['amount'])
            yield row


@dlt.resource(name='support_tickets', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_support_tickets():
    """Load support_tickets from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'support_tickets.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['ticket_id'] = int(row['ticket_id'])
            row['customer_id'] = int(row['customer_id'])
            yield row


@dlt.resource(name='ticket_resolutions', write_disposition='replace', schema_contract={'tables': 'evolve', 'columns': 'evolve', 'data_type': 'evolve'})
def load_ticket_resolutions():
    """Load ticket_resolutions from CSV."""
    import csv
    csv_path = SOURCE_DATA_DIR / 'ticket_resolutions.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['resolution_id'] = int(row['resolution_id'])
            row['ticket_id'] = int(row['ticket_id'])
            row['resolved_by'] = int(row['resolved_by'])
            yield row


def main():
    """Run the sales pipeline."""
    # Create the pipeline with explicit DuckDB credentials
    pipeline = dlt.pipeline(
        pipeline_name='sales_pipeline',
        destination=dlt.destinations.duckdb(credentials=DUCKDB_PATH),
        dataset_name='bronze',
    )

    # Load all resources
    load_info = pipeline.run([
        load_territories(),
        load_channels(),
        load_sales_reps(),
        load_customers(),
        load_contacts(),
        load_customer_addresses(),
        load_customer_segments(),
        load_product_categories(),
        load_products(),
        load_licenses(),
        load_pricing_tiers(),
        load_opportunities(),
        load_quotes(),
        load_orders(),
        load_order_lines(),
        load_invoices(),
        load_invoice_lines(),
        load_payments(),
        load_support_tickets(),
        load_ticket_resolutions(),
    ])

    print(f"\n✓ Pipeline sales_pipeline load step completed successfully")
    print(f"✓ Loaded {len(load_info.loads_ids)} load packages")
    print(f"✓ Tables created: {list(load_info.load_packages[0].schema_update.keys()) if load_info.load_packages else 'See .dlt/_load_info for details'}")
    return load_info


if __name__ == '__main__':
    main()
