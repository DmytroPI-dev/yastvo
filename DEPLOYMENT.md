# Deployment Configuration Guide

This document explains how to configure GitHub Actions secrets and variables for deploying the Yastvo Django application.

## GitHub Repository Variables

Go to **Settings → Secrets and variables → Actions → Variables** and add:

- `APP_NAME` (default: `cafe`)
  - The application name used for service naming and directories
  
- `SUBDOMAIN` (default: `cafe`)
  - The subdomain for your domain (e.g., `cafe` for `cafe.yourdomain.com`)

## GitHub Repository Secrets

Go to **Settings → Secrets and variables → Actions → Secrets** and add:

### SSH Access
- `ORACLE_SSH_KEY`
  - Your private SSH key for accessing the VM
  - Format: Complete private key including `-----BEGIN` and `-----END` lines

- `ORACLE_USER`
  - SSH username for the VM (e.g., `ubuntu` or your username)

- `ORACLE_HOST`
  - VM IP address or hostname

### Domain & SSL
- `DOMAIN_NAME`
  - Your domain name (e.g., `example.com`)
  - Combined with SUBDOMAIN to form full domain (e.g., `cafe.example.com`)

- `EMAIL`
  - Email address for Let's Encrypt SSL certificates

### Database
- `DB_PASSWORD`
  - Password for the MariaDB database user
  - Will be used to create `cafe_db` database with `cafe_user`

### Django Environment
- `BACKEND_ENV_VARS`
  - Complete `.env` file content for Django application
  - Example format:
    ```
    SECRET_KEY=your-django-secret-key-here
    DEBUG=False
    ALLOWED_HOSTS=cafe.example.com
    
    DB_ENGINE=django.db.backends.mysql
    DB_NAME=cafe_db
    DB_USER=cafe_user
    DB_PASSWORD=your-db-password-here
    DB_HOST=localhost
    DB_PORT=3306
    
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=your-admin-password-here
    
    # Add any other environment variables your app needs
    ```

## Pre-deployment Checklist

Before running the workflow, ensure:

1. ✅ Domain A record points to your VM IP address
2. ✅ VM has ports 80 and 443 open in firewall
3. ✅ SSH access is configured and working
4. ✅ All secrets and variables are set in GitHub
5. ✅ The VM has sufficient disk space and resources

## Infrastructure Notes

Since this VM already hosts another application (dormed), the deployment scripts are designed to:

- **Reuse existing infrastructure**: MariaDB, Nginx, Certbot are already installed
- **Create separate resources**: New database, new Gunicorn service, new Nginx site config
- **Avoid conflicts**: Each app runs its own Gunicorn service on its own socket

## Deployment Scripts

The deployment process uses three scripts:

1. **provision_infrastructure.sh**
   - Checks and installs system dependencies if needed
   - Creates new MariaDB database for this app
   - Configures SSL certificate for the domain
   - Sets up Nginx site configuration

2. **setup_gunicorn.sh**
   - Creates systemd service for Gunicorn
   - Configures service to run as a daemon

3. **deploy_app.sh**
   - Extracts application code
   - Sets up Python virtual environment
   - Installs dependencies
   - Runs migrations and collectstatic
   - Compiles translations
   - Restarts Gunicorn service

## Troubleshooting

If deployment fails, SSH into the VM and check:

```bash
# Check Gunicorn service status
sudo systemctl status cafe.service

# View service logs
sudo journalctl -u cafe.service -n 50

# Check Nginx configurationsudo nginx -t

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Check if database was created
sudo mysql -e "SHOW DATABASES LIKE 'cafe_db';"
```

## Manual Deployment

If you need to deploy manually:

```bash
# SSH into the VM
ssh user@your-vm-ip

# Navigate to project directory
cd ~/cafe

# Activate virtual environment
source venv/bin/activate

# Pull latest changes (if using git directly)
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart cafe.service
```
