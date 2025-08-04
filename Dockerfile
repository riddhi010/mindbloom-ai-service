# Base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# Expose the default HF Spaces port
EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"]
