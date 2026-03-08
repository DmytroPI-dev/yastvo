#!/bin/bash
set -e

# This script provisions the infrastructure: system dependencies, Nginx, SSL, and database
# It checks if things already exist before creating them (idempotent)
# Since infrastructure is already set up for existing app, this script is more cautious

echo "=== Provisioning Infrastructure for ${APP_NAME} ==="

# Check & Install System Dependencies (if needed)
echo "Checking system dependencies..."
PACKAGES_TO_CHECK="nginx mariadb-server libmariadb-dev-compat libmariadb-dev build-essential python3-venv python3-dev pkg-config"
MISSING_PACKAGES=""

for pkg in $PACKAGES_TO_CHECK; do
  if ! dpkg -l | grep -q "^ii  $pkg "; then
    MISSING_PACKAGES="$MISSING_PACKAGES $pkg"
  fi
done

if [ -n "$MISSING_PACKAGES" ]; then
  echo "Installing missing system dependencies: $MISSING_PACKAGES"
  sudo apt-get update -y
  sudo apt-get install -y $MISSING_PACKAGES
else
  echo "All system dependencies already installed."
fi

# Configure MariaDB - Create new database for this app
echo "=== Configuring MariaDB Database ==="
sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
sudo mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
echo "Database ${DB_NAME} configured successfully."

# Check SSL Certificate
echo "=== Checking SSL Certificate ==="
if ! command -v certbot >/dev/null 2>&1; then
  echo "Installing certbot..."
  sudo apt-get install -y certbot python3-certbot-nginx
fi

if sudo certbot certificates 2>/dev/null | grep -q "Domains: $DOMAIN_FQDN"; then
  echo "SSL certificate for $DOMAIN_FQDN already exists."
else
  echo "Requesting new SSL certificate for $DOMAIN_FQDN..."
  sudo certbot --nginx -d "$DOMAIN_FQDN" --agree-tos --email "$EMAIL" --non-interactive
fi

# Configure Nginx - Create new site configuration
echo "=== Configuring Nginx ==="
if [ ! -f "/etc/nginx/sites-available/${APP_NAME}" ]; then
  echo "Creating Nginx configuration for ${APP_NAME}..."
  sudo tee /etc/nginx/sites-available/${APP_NAME} > /dev/null <<NGINX_CONF
server {
    listen 80;
    server_name ${DOMAIN_FQDN};
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name ${DOMAIN_FQDN};

    ssl_certificate /etc/letsencrypt/live/${DOMAIN_FQDN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN_FQDN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Increase max upload size for images and files
    client_max_body_size 5M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias ${PROJECT_DIR}/static/;
    }

    location /media/ {
        alias ${PROJECT_DIR}/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:${PROJECT_DIR}/${APP_NAME}.sock;
    }
}
NGINX_CONF

  # Enable the site
  sudo ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/
  
  # Test nginx configuration
  sudo nginx -t
  
  # Reload nginx
  sudo systemctl reload nginx
  echo "Nginx configuration created and enabled for ${APP_NAME}."
else
  echo "Nginx configuration for ${APP_NAME} already exists. Skipping creation."
  # Still reload nginx in case config changed
  sudo nginx -t && sudo systemctl reload nginx
fi

echo "=== Infrastructure provisioning complete for ${APP_NAME} ==="
