#!/bin/bash
set -e

# Create necessary directories
mkdir -p config addons

# Copy the Odoo configuration file
cat > config/odoo.conf << 'EOL'
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
db_name = postgres
http_port = 8069
EOL

# Start the containers
docker-compose up -d

















