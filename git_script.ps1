$GitPath = "C:\Program Files\Git\cmd\git.exe"

& $GitPath init

# Add remote, ignore error if it already exists
& $GitPath remote add origin https://github.com/maqboolhussain914-ops/Paradise-Nursery-Online-Plant-Seed-Store.git

# Set user name and email just in case
& $GitPath config user.name "Maqbool Hussain"
& $GitPath config user.email "maqbool@example.com"

# Milestone 2
& $GitPath add NORMALIZATION.md
& $GitPath commit -m "M2: Applied 2NF and 3NF normalization, updated ERD and schema"

# Milestone 3
& $GitPath add users.csv categories.csv products.csv orders.csv order_items.csv cart.csv cart_items.csv DATAFLOW.md generate_data.py
& $GitPath commit -m "M3: Synthetic data generated; dataflow documented"

# Milestone 4
& $GitPath add schema.sql
& $GitPath commit -m "M4: DDL scripts added, EER diagram verified"

# Milestone 5
& $GitPath add data_load.sql
& $GitPath commit -m "M5: Data populated validation queries added"

# Other files
& $GitPath add .
& $GitPath commit -m "Add final pdf contents and extra files"

# Push to main
Write-Host "Pushing to remote... A login prompt may appear!"
& $GitPath push -u origin main --force
