FROM python:3.9

# Create a non-root user for safety
RUN useradd -m appuser
WORKDIR /home/appuser/app

# Copy your project files
COPY --chown=appuser:appuser . .

# Install dependencies globally (no PATH warning)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt && \
    ln -s /home/appuser/.local/bin/* /usr/local/bin/

# Switch to non-root user
USER appuser

EXPOSE 5000

# Run Gunicorn (production server)
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
