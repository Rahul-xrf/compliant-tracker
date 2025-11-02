FROM python:3.11-slim

# Create and switch to a non-root user
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser/app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy rest of the code
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
