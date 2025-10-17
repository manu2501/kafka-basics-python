# Burger Kiosk API with FastAPI and Kafka

A burger kiosk application built with FastAPI for the web API and Apache Kafka for message queuing. This application demonstrates how to build a real-time order processing system using modern Python web frameworks and event streaming.

## Features

- 🍔 Full burger menu with various options (Classic, Cheese, Bacon, Veggie, etc.)
- 🛍️ Real-time order processing with Kafka
- 📝 Order tracking and status updates
- 🔄 Asynchronous message processing
- 📊 FastAPI automatic OpenAPI documentation
- 🐳 Docker Compose for easy deployment

## Project Structure

- `main.py` — FastAPI application with endpoints for viewing menu and placing orders
- `models.py` — Pydantic models for burgers, orders, and API responses
- `producer.py` — Kafka producer for sending orders to the message queue
- `tracker.py` — Order tracking consumer that displays incoming orders
- `docker-compose.yaml` — Kafka broker configuration (KRaft mode)
- `pyproject.toml` — Project dependencies and metadata

## Requirements

- Python 3.10 or newer
- Docker and Docker Compose
- pip and virtualenv (recommended)

Dependencies:
- FastAPI and Uvicorn for the web API
- confluent-kafka for Kafka integration
- Pydantic for data validation

Note: On Windows, installing `confluent-kafka` may require WSL or Docker if you encounter build issues.

## Quickstart

1. Start Kafka with Docker Compose:

```powershell
docker-compose up -d
```

2. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

3. Start the FastAPI application:

```powershell
python main.py
```

The API will be available at http://localhost:8000. Visit http://localhost:8000/docs for the interactive API documentation.

4. In another terminal, start the order tracker:

```powershell
python tracker.py
```

## API Endpoints

### GET /menu
Get the full menu of available burgers.

Response example:
```json
[
  {
    "id": 1,
    "name": "Classic Burger",
    "description": "A juicy beef patty with lettuce, tomato, and our special sauce",
    "price": 8.99,
    "size": "Regular",
    "is_available": true
  }
]
```

### GET /menu/{burger_id}
Get details of a specific burger by ID.

### POST /order
Place a new burger order.

Request body example:
```json
{
  "items": [
    {
      "burger_id": 1,
      "quantity": 2,
      "special_instructions": "Extra cheese please"
    }
  ],
  "customer_name": "John Doe",
  "total_amount": 0
}
```

Response example:
```json
{
  "order_id": "uuid-here",
  "status": "accepted",
  "estimated_wait_time": 15,
  "message": "Your order has been accepted and is being processed"
}
```

## Configuration

- Broker address: both `producer.py` and `tracker.py` default to `localhost:9092` via the `bootstrap.servers` setting. If your broker runs elsewhere, update `producer_config` and `consumer_config` accordingly.
- Topic: `orders` (hard-coded in both producer and consumer in this example).

## Files overview

- `producer.py` — builds a JSON `order` dict, serializes it with `json.dumps(...).encode('utf-8')`, and uses `Producer.produce(topic, value=...)` with a callback `delivery_report` to print delivery status. Finally, it calls `producer.flush()` to ensure delivery.
- `tracker.py` — creates a `Consumer`, subscribes to `['orders']`, polls in a loop and prints decoded JSON messages. It handles `KeyboardInterrupt` gracefully by closing the consumer.
- `docker-compose.yaml` — example KRaft single-node configuration. It exposes PLAINTEXT on port 9092 and sets controller listener on 9093. This setup is intended for local experiments and not production.

## Troubleshooting

- Kafka not reachable:
	- Ensure Docker is running and `docker-compose up -d` succeeded.
	- Check container logs: `docker-compose logs kafka`.
	- Confirm port 9092 is listening on the host: `docker ps` and `netstat -an`.
- confluent-kafka install fails on Windows:
	- Use WSL (Ubuntu) and install inside WSL, or run producer/consumer in a Linux container.
	- Ensure you have a compatible Python version and a pre-built wheel for `confluent-kafka`.
- Consumer shows no messages:
	- Confirm the producer successfully delivered a message (delivery callback or logs).
	- Ensure `auto.offset.reset` in `tracker.py` is set appropriately (`earliest` to read from beginning).

## Development notes

- To package/install locally, `pyproject.toml` is provided. Install in editable/developer mode with `python -m pip install -e .`.
- There's no automated test suite in this example. Adding unit tests and a CI job would be a good next step.

## Next steps / Ideas

- Add CLI flags or a configuration file to set brokers, topics and message payloads.
- Add schema validation (e.g., Avro / JSON Schema) for the order payload.
- Add retries and error handling in the producer for robustness.
