# Modular Burger Kiosk (Python FastAPI + Kafka)

This repo now includes a modular, service-based backend using FastAPI and Kafka with simple admin and user dashboards.

## Services
- user_service (FastAPI): menu + order API, produces to Kafka topic `burger-orders`, serves a simple user dashboard at `/`.
- admin_service (FastAPI): consumes `burger-orders`, exposes `/metrics` and Server-Sent Events at `/events`, serves admin dashboard at `/`.
- gateway (FastAPI): simple reverse proxy for `/user/*` and `/admin/*` to reach services from a single port.
- kafka: single-broker Kafka (KRaft mode) via Docker.

## Run (Docker Compose)

```bash
docker compose -f docker-compose.services.yaml up --build
```

Then open:
- Gateway: http://localhost:8080
  - User Dashboard: http://localhost:8080/user/
  - Admin Dashboard: http://localhost:8080/admin/
- Direct services (optional):
  - User Service: http://localhost:8001
  - Admin Service: http://localhost:8002

## Notes
- Services use `KAFKA_BOOTSTRAP` env (defaults to `localhost:9092`) and are wired to `kafka:9092` in Compose.
- This keeps existing single-service demo files intact. New services live under `services/`.
