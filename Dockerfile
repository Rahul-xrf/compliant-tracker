FROM python:3.9

# Create non-root user
RUN useradd -m appuser
WORKDIR /home/appuser/app

# Copy project files
COPY --chown=appuser:appuser . .

# Install Python dependencies for the non-root user
RUN pip install --no-cache-dir --user -r requirements.txt && \
    ln -s /home/appuser/.local/bin/* /usr/local/bin/

# Switch to non-root user for security
USER appuser

EXPOSE 5000

# Start Gunicorn server
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
