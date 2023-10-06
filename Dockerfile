# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables (modify as needed)
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Yastvo.settings

# Create and set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install project dependencies
RUN pip install -r requirements.txt

# Expose the port Gunicorn will run on
EXPOSE 8000

# Start Gunicorn
#CMD ["gunicorn", "Yastvo.wsgi:application", "--bind", "127.0.0.1:8000"]
CMD ["gunicorn", "Yastvo.wsgi:application", "--bind", "0.0.0.0:8000"]

