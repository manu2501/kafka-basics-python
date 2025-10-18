# Burger Ordering System (FastAPI + Postgres + Nginx)

## Structure
- `backend/` FastAPI app with JWT auth, admin, user flows and Postgres
- `frontend/` Nginx serving static admin and user dashboards consuming the backend API
- `docker-compose.yaml` One-click stack: Postgres, backend, frontend, e2e test container

## Run
```bash
docker compose up --build
```
- Backend API: `http://localhost:8000/docs`
- Frontend (user): `http://localhost:8080/`
- Frontend (admin): `http://localhost:8080/admin/`

## Admin flow
- Login at admin page (defaults: username `admin`, password `admin123` seeded on startup)
- Add burger SKUs, update availability/price, view and update order statuses

## User flow
- Register/Login at user page
- View menu, add to cart, place order
- View own orders and statuses

## Notes
- DB url is configured via `DB_URL` env in backend service; default uses `db` service credentials.
- JWT secret set via `JWT_SECRET` env (dev default in compose).
- On backend startup: tables are created, default admin user and sample SKUs are seeded.

## E2E test
Runs automatically as `e2e` container:
- Registers and logs in a user
- Fetches menu and places an order
- Logs in as admin and completes the order
- Prints `E2E OK` on success
