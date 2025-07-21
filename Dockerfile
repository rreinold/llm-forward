FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install uv && \
    uv sync --frozen

# Copy application code
COPY llm_proxy/ ./llm_proxy/

# Expose port
EXPOSE 80

# Set environment variable for uvicorn
ENV PYTHONPATH=/app

# Run with uv run
CMD ["uv", "run", "uvicorn", "llm_proxy.main:create_app", "--host", "0.0.0.0", "--port", "80"] 
