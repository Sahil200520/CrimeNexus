# Use supported Python 3.10 runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including OpenJDK (required for H2O AutoML)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre-headless \
    build-essential \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt-get/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and modules
COPY app/ /app/app/
COPY assets/ /app/assets/
COPY models/ /app/models/
COPY pipelines/ /app/pipelines/
COPY Component_datasets/ /app/Component_datasets/
COPY Crime_Pattern_Analysis/ /app/Crime_Pattern_Analysis/
COPY Criminal_Profiling/ /app/Criminal_Profiling/
COPY Predictive_Modeling/ /app/Predictive_Modeling/
COPY Resource_Allocation/ /app/Resource_Allocation/
COPY Continuous_learning_and_feedback/ /app/Continuous_learning_and_feedback/

# Set Python path so imports resolve cleanly across directories
ENV PYTHONPATH="/app:/app/app:${PYTHONPATH}"

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit with fixed entrypoint path and network binding
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
