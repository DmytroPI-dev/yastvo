#!/bin/bash
set -e

# This script sets up the Gunicorn systemd service if it doesn't exist
# Creates a separate service for this Django application

echo "=== Setting up Gunicorn systemd service for ${APP_NAME} ==="

if [ ! -f /etc/systemd/system/${APP_NAME}.service ]; then
  echo "Creating Gunicorn service file..."
  sudo tee /etc/systemd/system/${APP_NAME}.service > /dev/null <<GUNICORN_SERVICE
[Unit]
Description=gunicorn daemon for ${APP_NAME}
After=network.target

[Service]
User=${DEPLOY_USER}
Group=www-data
WorkingDirectory=${PROJECT_DIR}
ExecStart=${VENV_DIR}/bin/gunicorn --workers 3 --bind unix:${PROJECT_DIR}/${APP_NAME}.sock Yastvo.wsgi:application

[Install]
WantedBy=multi-user.target
GUNICORN_SERVICE

  sudo systemctl daemon-reload
  sudo systemctl enable ${APP_NAME}.service
  echo "Gunicorn service created and enabled for ${APP_NAME}."
else
  echo "Gunicorn service file for ${APP_NAME} already exists."
  # Reload daemon in case the service file was updated
  sudo systemctl daemon-reload
fi

echo "=== Gunicorn setup complete for ${APP_NAME} ==="
