# Kafka Example (Kafka + Python producer/consumer)

This small example demonstrates a minimal Kafka producer and consumer implemented in Python using the confluent-kafka client, plus a Docker Compose configuration for running a single-node Kafka broker in KRaft mode.

The repository contains:

- `producer.py` — simple producer that sends a single JSON order to the `orders` topic.
- `tracker.py` — simple consumer that subscribes to the `orders` topic and prints received orders.
- `main.py` — trivial entrypoint (prints a greeting). Useful for a quick smoke check.
- `docker-compose.yaml` — starts a single Kafka broker (KRaft mode) exposed on localhost:9092.
- `pyproject.toml` — project metadata and dependency on `confluent-kafka`.

## Requirements

- Python 3.10 or newer
- Docker (for running the Kafka broker via Docker Compose)
- uv (recommended)
- On Windows, installing `confluent-kafka` may require a compatible wheel or WSL; if you run into build issues, use WSL or run the producer/consumer inside a Linux container.

Note: `confluent-kafka` depends on librdkafka. On most platforms `pip install confluent-kafka` will fetch a pre-built wheel. If pip attempts to compile librdkafka and fails, follow platform-specific instructions (or use WSL/Docker).

## Quickstart (recommended)

1. Start Kafka with Docker Compose:

```powershell
docker-compose up -d
```

This uses the `confluentinc/cp-kafka:latest` image and exposes the broker on `localhost:9092`.

2. (Optional) Create a Python virtual environment and install dependencies:

```powershell
uv sync
```

Or install the dependency directly:

```powershell
uv pip install confluent-kafka
```

3. Start the consumer (tracker) in one terminal to listen for orders:

```powershell
python tracker.py
```

You should see:

```
Listening for messages on 'orders' topic...
```

4. Run the producer in another terminal to send one sample order:

```powershell
python producer.py
```

The producer will attempt to deliver a single JSON message to the `orders` topic. The consumer should print the received order.

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
