from confluent_kafka import Producer
import json
from models import Order

producer_config = {"bootstrap.servers": "localhost:9092"}
producer = Producer(producer_config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
        return False
    else:
        print(f"Message delivered to topic {msg.topic()}")
        print(f"Partition: {msg.partition()}, Offset: {msg.offset()}")
        return True


async def send_order_to_kafka(order: Order) -> bool:
    try:
        # Convert order to dict and encode as JSON
        order_dict = order.model_dump()
        # Convert UUID to string for JSON serialization
        order_dict["order_id"] = str(order_dict["order_id"])
        # Convert datetime to ISO format string
        order_dict["created_at"] = order_dict["created_at"].isoformat()

        # Encode as JSON bytes
        value = json.dumps(order_dict).encode("utf-8")

        # Produce to Kafka
        producer.produce("burger-orders", value=value, callback=delivery_report)

        # Wait for message to be delivered
        producer.flush(timeout=5)
        return True

    except Exception as e:
        print(f"Failed to send order to Kafka: {e}")
        return False
