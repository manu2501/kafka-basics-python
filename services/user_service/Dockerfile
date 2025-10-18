FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
# Install deps for this service
COPY services/user_service/requirements.txt /app/services/user_service/requirements.txt
RUN pip install --no-cache-dir -r /app/services/user_service/requirements.txt

# Copy shared and service code
COPY services/shared /app/services/shared
COPY services/user_service /app/services/user_service

WORKDIR /app/services/user_service
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
