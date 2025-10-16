from confluent_kafka import Producer
import uuid
import json

producer_config = {"bootstrap.servers": "localhost:9092"}

producer = Producer(producer_config)

order = {
    "order_id": str(uuid.uuid4()),
    "user": "manoj",
    "item": "Chicken Sandwich",
    "quantity": 1200,
    "price": 5.99,
}


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.value().decode('utf-8')}")
        print(
            f"Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}"
        )


value = json.dumps(order).encode("utf-8")
producer.produce("orders", value=value, callback=delivery_report)
producer.flush()
