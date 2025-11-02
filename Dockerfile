# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Run Gunicorn to serve Flask app
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
