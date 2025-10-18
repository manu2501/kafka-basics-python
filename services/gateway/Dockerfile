FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY services/gateway/requirements.txt /app/services/gateway/requirements.txt
RUN pip install --no-cache-dir -r /app/services/gateway/requirements.txt
COPY services/gateway /app/services/gateway
WORKDIR /app/services/gateway
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
