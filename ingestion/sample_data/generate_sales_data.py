#!/usr/bin/env python3
"""Generate synthetic IT business sales data with referential integrity."""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 100
NUM_CONTACTS = 200
NUM_CUSTOMER_ADDRESSES = 80
NUM_CUSTOMER_SEGMENTS = 120
NUM_PRODUCTS = 50
NUM_CATEGORIES = 10
NUM_LICENSES = 40
NUM_PRICING_TIERS = 100
NUM_OPPORTUNITIES = 200
NUM_QUOTES = 150
NUM_ORDERS = 150
NUM_ORDER_LINES = 300
NUM_SALES_REPS = 10
NUM_INVOICES = 120
NUM_INVOICE_LINES = 250
NUM_PAYMENTS = 100
NUM_SUPPORT_TICKETS = 50
NUM_TICKET_RESOLUTIONS = 40
NUM_TERRITORIES = 5
NUM_CHANNELS = 3

def write_csv(filename, data, fieldnames):
    """Write data to CSV file."""
    with open(f'/workspace/ingestion/sample_data/{filename}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ {filename}.csv: {len(data)} rows")

# 1. Territories
territories = []
territory_names = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
regions = ['Americas', 'EMEA', 'APAC', 'LATAM', 'MEA']
for i in range(NUM_TERRITORIES):
    territories.append({
        'territory_id': i + 1,
        'territory_name': territory_names[i],
        'region': regions[i],
        'country': fake.country()
    })
write_csv('territories', territories, ['territory_id', 'territory_name', 'region', 'country'])

# 2. Channels
channels = [
    {'channel_id': 1, 'channel_name': 'Direct Sales', 'channel_type': 'direct', 'commission_rate': 0.05},
    {'channel_id': 2, 'channel_name': 'Partner Network', 'channel_type': 'indirect', 'commission_rate': 0.15},
    {'channel_id': 3, 'channel_name': 'Online Store', 'channel_type': 'ecommerce', 'commission_rate': 0.03}
]
write_csv('channels', channels, ['channel_id', 'channel_name', 'channel_type', 'commission_rate'])

# 3. Sales Reps
sales_reps = []
for i in range(NUM_SALES_REPS):
    sales_reps.append({
        'sales_rep_id': i + 1,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'territory_id': random.randint(1, NUM_TERRITORIES),
        'hire_date': fake.date_between(start_date='-5y', end_date='-1y')
    })
write_csv('sales_reps', sales_reps, ['sales_rep_id', 'first_name', 'last_name', 'email', 'territory_id', 'hire_date'])

# 4. Customers
customers = []
industries = ['Software', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Government']
for i in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': i + 1,
        'company_name': fake.company(),
        'industry': random.choice(industries),
        'country': fake.country(),
        'created_date': fake.date_between(start_date='-3y', end_date='-1m'),
        'is_active': random.choice([True, True, True, False])  # 75% active
    })
write_csv('customers', customers, ['customer_id', 'company_name', 'industry', 'country', 'created_date', 'is_active'])

# 5. Contacts
contacts = []
for i in range(NUM_CONTACTS):
    contacts.append({
        'contact_id': i + 1,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'role': random.choice(['IT Manager', 'CTO', 'Procurement', 'CEO', 'Director'])
    })
write_csv('contacts', contacts, ['contact_id', 'customer_id', 'first_name', 'last_name', 'email', 'phone', 'role'])

# 6. Customer Addresses
customer_addresses = []
address_types = ['Billing', 'Shipping', 'Headquarters']
for i in range(NUM_CUSTOMER_ADDRESSES):
    customer_addresses.append({
        'address_id': i + 1,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'address_type': random.choice(address_types),
        'street': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'postal_code': fake.postcode()
    })
write_csv('customer_addresses', customer_addresses, ['address_id', 'customer_id', 'address_type', 'street', 'city', 'state', 'postal_code'])

# 7. Customer Segments
customer_segments = []
segment_types = ['Company Size', 'Revenue Band', 'Industry Vertical', 'Geographic']
segment_values = {
    'Company Size': ['SMB', 'Mid-Market', 'Enterprise'],
    'Revenue Band': ['0-1M', '1-10M', '10-50M', '50M+'],
    'Industry Vertical': industries,
    'Geographic': ['North', 'South', 'East', 'West', 'International']
}
for i in range(NUM_CUSTOMER_SEGMENTS):
    seg_type = random.choice(segment_types)
    customer_segments.append({
        'segment_id': i + 1,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'segment_type': seg_type,
        'segment_value': random.choice(segment_values[seg_type]),
        'effective_date': fake.date_between(start_date='-2y', end_date='today')
    })
write_csv('customer_segments', customer_segments, ['segment_id', 'customer_id', 'segment_type', 'segment_value', 'effective_date'])

# 8. Product Categories
product_categories = []
category_names = [
    'Hardware', 'Software', 'Cloud Services', 'Consulting', 'Support & Maintenance',
    'Training', 'Security Solutions', 'Data Analytics', 'AI/ML Tools', 'Integration Services'
]
for i in range(NUM_CATEGORIES):
    product_categories.append({
        'category_id': i + 1,
        'category_name': category_names[i],
        'parent_category_id': None if i < 3 else random.randint(1, 3),
        'description': fake.sentence()
    })
write_csv('product_categories', product_categories, ['category_id', 'category_name', 'parent_category_id', 'description'])

# 9. Products
products = []
product_types = ['Hardware', 'Software License', 'SaaS Subscription', 'Professional Services']
for i in range(NUM_PRODUCTS):
    products.append({
        'product_id': i + 1,
        'product_name': f"{fake.catch_phrase()} {random.choice(['Pro', 'Enterprise', 'Lite', 'Ultimate'])}",
        'product_type': random.choice(product_types),
        'category_id': random.randint(1, NUM_CATEGORIES),
        'list_price': round(random.uniform(500, 50000), 2),
        'is_active': random.choice([True, True, True, False])
    })
write_csv('products', products, ['product_id', 'product_name', 'product_type', 'category_id', 'list_price', 'is_active'])

# 10. Licenses
licenses = []
license_types = ['Perpetual', 'Annual', 'Monthly', 'Trial']
for i in range(NUM_LICENSES):
    lic_type = random.choice(license_types)
    duration = {
        'Perpetual': None,
        'Annual': 12,
        'Monthly': 1,
        'Trial': 3
    }[lic_type]
    licenses.append({
        'license_id': i + 1,
        'product_id': random.randint(1, NUM_PRODUCTS),
        'license_type': lic_type,
        'duration_months': duration,
        'max_users': random.choice([1, 5, 10, 25, 50, 100, None])
    })
write_csv('licenses', licenses, ['license_id', 'product_id', 'license_type', 'duration_months', 'max_users'])

# 11. Pricing Tiers
pricing_tiers = []
for i in range(NUM_PRICING_TIERS):
    min_qty = random.choice([1, 5, 10, 25, 50, 100])
    max_qty = min_qty * random.randint(2, 10)
    base_price = random.uniform(100, 5000)
    discount = random.uniform(0.05, 0.30)
    pricing_tiers.append({
        'tier_id': i + 1,
        'product_id': random.randint(1, NUM_PRODUCTS),
        'min_quantity': min_qty,
        'max_quantity': max_qty,
        'unit_price': round(base_price * (1 - discount), 2)
    })
write_csv('pricing_tiers', pricing_tiers, ['tier_id', 'product_id', 'min_quantity', 'max_quantity', 'unit_price'])

# 12. Opportunities
opportunities = []
stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
for i in range(NUM_OPPORTUNITIES):
    stage = random.choice(stages)
    probability = {
        'Prospecting': 0.1,
        'Qualification': 0.25,
        'Proposal': 0.50,
        'Negotiation': 0.75,
        'Closed Won': 1.0,
        'Closed Lost': 0.0
    }[stage]
    close_date = fake.date_between(start_date='-1y', end_date='+6m') if stage != 'Prospecting' else fake.date_between(start_date='today', end_date='+1y')
    opportunities.append({
        'opportunity_id': i + 1,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'sales_rep_id': random.randint(1, NUM_SALES_REPS),
        'stage': stage,
        'value': round(random.uniform(5000, 500000), 2),
        'close_date': close_date,
        'probability': probability
    })
write_csv('opportunities', opportunities, ['opportunity_id', 'customer_id', 'sales_rep_id', 'stage', 'value', 'close_date', 'probability'])

# 13. Quotes
quotes = []
statuses = ['Draft', 'Sent', 'Accepted', 'Rejected', 'Expired']
closed_opps = [o for o in opportunities if o['stage'] in ['Closed Won', 'Negotiation', 'Proposal']]
for i in range(NUM_QUOTES):
    opp = random.choice(closed_opps) if closed_opps else opportunities[0]
    quote_date = fake.date_between(start_date='-1y', end_date='today')
    valid_days = random.randint(15, 90)
    quotes.append({
        'quote_id': i + 1,
        'opportunity_id': opp['opportunity_id'],
        'quote_date': quote_date,
        'valid_until': quote_date + timedelta(days=valid_days),
        'total_amount': round(opp['value'] * random.uniform(0.9, 1.1), 2),
        'status': random.choice(statuses)
    })
write_csv('quotes', quotes, ['quote_id', 'opportunity_id', 'quote_date', 'valid_until', 'total_amount', 'status'])

# 14. Orders
orders = []
won_opps = [o for o in opportunities if o['stage'] == 'Closed Won']
for i in range(NUM_ORDERS):
    opp = random.choice(won_opps) if won_opps else opportunities[0]
    order_date = opp['close_date'] if isinstance(opp['close_date'], str) else fake.date_between(start_date='-1y', end_date='today')
    orders.append({
        'order_id': i + 1,
        'customer_id': opp['customer_id'],
        'sales_rep_id': opp['sales_rep_id'],
        'order_date': order_date,
        'total_amount': round(opp['value'] * random.uniform(0.95, 1.05), 2),
        'status': random.choice(['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled'])
    })
write_csv('orders', orders, ['order_id', 'customer_id', 'sales_rep_id', 'order_date', 'total_amount', 'status'])

# 15. Order Lines
order_lines = []
for i in range(NUM_ORDER_LINES):
    order = random.choice(orders)
    product = random.choice(products)
    quantity = random.randint(1, 50)
    unit_price = product['list_price'] * random.uniform(0.8, 1.0)  # Some discount
    order_lines.append({
        'order_line_id': i + 1,
        'order_id': order['order_id'],
        'line_number': (i % 3) + 1,  # 1-3 lines per order typically
        'product_id': product['product_id'],
        'quantity': quantity,
        'unit_price': round(unit_price, 2),
        'line_total': round(quantity * unit_price, 2)
    })
write_csv('order_lines', order_lines, ['order_line_id', 'order_id', 'line_number', 'product_id', 'quantity', 'unit_price', 'line_total'])

# 16. Invoices
invoices = []
confirmed_orders = [o for o in orders if o['status'] in ['Confirmed', 'Shipped', 'Delivered']]
for i in range(NUM_INVOICES):
    order = random.choice(confirmed_orders) if confirmed_orders else orders[0]
    invoice_date = order['order_date'] if isinstance(order['order_date'], str) else fake.date_between(start_date='-1y', end_date='today')
    if isinstance(invoice_date, str):
        invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d').date()
    due_days = random.choice([15, 30, 45, 60])
    invoices.append({
        'invoice_id': i + 1,
        'order_id': order['order_id'],
        'invoice_date': invoice_date,
        'due_date': invoice_date + timedelta(days=due_days),
        'total_amount': order['total_amount'],
        'status': random.choice(['Draft', 'Sent', 'Paid', 'Overdue', 'Cancelled'])
    })
write_csv('invoices', invoices, ['invoice_id', 'order_id', 'invoice_date', 'due_date', 'total_amount', 'status'])

# 17. Invoice Lines
invoice_lines = []
for i in range(NUM_INVOICE_LINES):
    invoice = random.choice(invoices)
    # Find order lines for this invoice's order
    related_order_lines = [ol for ol in order_lines if ol['order_id'] == invoice['order_id']]
    if related_order_lines:
        order_line = random.choice(related_order_lines)
        invoice_lines.append({
            'invoice_line_id': i + 1,
            'invoice_id': invoice['invoice_id'],
            'line_number': (i % 3) + 1,
            'product_id': order_line['product_id'],
            'quantity': order_line['quantity'],
            'unit_price': order_line['unit_price'],
            'line_total': order_line['line_total']
        })
write_csv('invoice_lines', invoice_lines, ['invoice_line_id', 'invoice_id', 'line_number', 'product_id', 'quantity', 'unit_price', 'line_total'])

# 18. Payments
payments = []
paid_invoices = [inv for inv in invoices if inv['status'] == 'Paid']
for i in range(NUM_PAYMENTS):
    invoice = random.choice(paid_invoices) if paid_invoices else invoices[0]
    payment_date = invoice['invoice_date'] if isinstance(invoice['invoice_date'], datetime) else datetime.strptime(str(invoice['invoice_date']), '%Y-%m-%d').date()
    payment_date = payment_date + timedelta(days=random.randint(1, 45))
    payments.append({
        'payment_id': i + 1,
        'invoice_id': invoice['invoice_id'],
        'payment_date': payment_date,
        'amount': round(invoice['total_amount'] * random.uniform(0.3, 1.0), 2),  # Partial or full payment
        'payment_method': random.choice(['Wire Transfer', 'Credit Card', 'Check', 'ACH']),
        'status': random.choice(['Pending', 'Completed', 'Failed'])
    })
write_csv('payments', payments, ['payment_id', 'invoice_id', 'payment_date', 'amount', 'payment_method', 'status'])

# 19. Support Tickets
support_tickets = []
priorities = ['Low', 'Medium', 'High', 'Critical']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated']
categories = ['Bug', 'Feature Request', 'Configuration', 'Performance', 'Data Issue', 'Access']
for i in range(NUM_SUPPORT_TICKETS):
    created = fake.date_between(start_date='-6m', end_date='today')
    status = random.choice(statuses)
    resolved = None
    if status in ['Resolved', 'Closed']:
        if isinstance(created, str):
            created = datetime.strptime(created, '%Y-%m-%d').date()
        resolved = created + timedelta(days=random.randint(1, 30))
    support_tickets.append({
        'ticket_id': i + 1,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'created_date': created,
        'resolved_date': resolved,
        'priority': random.choice(priorities),
        'status': status,
        'category': random.choice(categories)
    })
write_csv('support_tickets', support_tickets, ['ticket_id', 'customer_id', 'created_date', 'resolved_date', 'priority', 'status', 'category'])

# 20. Ticket Resolutions
ticket_resolutions = []
resolved_tickets = [t for t in support_tickets if t['status'] in ['Resolved', 'Closed']]
for i in range(NUM_TICKET_RESOLUTIONS):
    ticket = random.choice(resolved_tickets) if resolved_tickets else support_tickets[0]
    ticket_resolutions.append({
        'resolution_id': i + 1,
        'ticket_id': ticket['ticket_id'],
        'resolved_by': random.choice([rep['sales_rep_id'] for rep in sales_reps]),
        'resolution_notes': fake.sentence(nb_words=10),
        'resolution_date': ticket.get('resolved_date', fake.date_this_month())
    })
write_csv('ticket_resolutions', ticket_resolutions, ['resolution_id', 'ticket_id', 'resolved_by', 'resolution_notes', 'resolution_date'])

print(f"\n✓ Successfully generated 20 CSV files with referential integrity")
print(f"Total records: {sum([len(d) for d in [territories, channels, sales_reps, customers, contacts, customer_addresses, customer_segments, product_categories, products, licenses, pricing_tiers, opportunities, quotes, orders, order_lines, invoices, invoice_lines, payments, support_tickets, ticket_resolutions]])}")
