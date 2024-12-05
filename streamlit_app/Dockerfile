FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    libpq-dev \
    python3-dev \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements .
RUN pip install --no-cache-dir -r private.txt
RUN pip install --no-cache-dir -r prod.txt


# Copy the rest of the application
COPY streamlit_app/ .


# Command to run the application
CMD ["streamlit", "run", "fcb_analytics.py", "--server.port=8501", "--server.address=0.0.0.0"]
