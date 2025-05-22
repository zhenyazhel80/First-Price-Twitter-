# Use official Python image
FROM python:3.11

# Create virtual environment
RUN python -m venv /opt/venv

# Set path to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies inside venv
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

RUN pip install --no-cache-dir -r requirements.txt
