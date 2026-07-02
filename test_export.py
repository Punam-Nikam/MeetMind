# test_export.py

from database import MongoDBHandler
from export import CSVExporter

print("="*60)
print("MEETMIND - CSV EXPORTER")
print("="*60)

# Step 1: Create a database handler
db = MongoDBHandler()

# Step 2: Create a CSV exporter using the database handler
exporter = CSVExporter(db)

# Step 3: Export ALL action items to 'all_actions.csv'
print("\nExporting ALL action items...")
exporter.export_all_actions("all_actions.csv")

# Step 4: Export ONLY pending action items to 'pending_actions.csv'
print("\nExporting PENDING action items...")
exporter.export_pending_actions("pending_actions.csv")

print("\nExport complete! Check folder for the CSV files.")