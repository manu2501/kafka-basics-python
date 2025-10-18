FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
# Install deps for this service
COPY services/admin_service/requirements.txt /app/services/admin_service/requirements.txt
RUN pip install --no-cache-dir -r /app/services/admin_service/requirements.txt

# Copy shared and service code
COPY services/shared /app/services/shared
COPY services/admin_service /app/services/admin_service

WORKDIR /app/services/admin_service
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
