FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Add /app/server to Python path so imports like
# "from environment import CyberEnvironment" work inside server/app.py
ENV PYTHONPATH="/app/server:/app"

# Expose port
EXPOSE 7860

# Run — matches HuggingFace Space structure where files are in server/
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
