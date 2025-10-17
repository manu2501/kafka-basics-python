from confluent_kafka import Consumer
import json
from datetime import datetime
from models import MENU_ITEMS

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "burger-tracker",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_config)
consumer.subscribe(["burger-orders"])

# Create a menu lookup for quick burger name resolution
menu_lookup = {item.id: item for item in MENU_ITEMS}

def format_order(order_data):
    """Format the order data into a nice display string"""
    order_str = "\n" + "="*50 + "\n"
    order_str += f"Order ID: {order_data['order_id']}\n"
    order_str += f"Customer: {order_data['customer_name']}\n"
    order_str += f"Ordered at: {datetime.fromisoformat(order_data['created_at']).strftime('%Y-%m-%d %H:%M:%S')}\n"
    order_str += "-"*30 + "\n"
    
    for item in order_data['items']:
        burger = menu_lookup.get(item['burger_id'])
        if burger:
            order_str += f"{item['quantity']}x {burger.name}"
            if item.get('special_instructions'):
                order_str += f" ({item['special_instructions']})"
            order_str += "\n"
    
    order_str += "-"*30 + "\n"
    order_str += f"Total Amount: ${order_data['total_amount']:.2f}\n"
    order_str += "="*50 + "\n"
    return order_str

print("🍔 Burger Order Tracking System")
print("Listening for orders on 'burger-orders' topic...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            order_data = json.loads(msg.value().decode('utf-8'))
            print("\n📝 New Order Received!")
            print(format_order(order_data))
        except json.JSONDecodeError as e:
            print(f"Error decoding order: {e}")
        except Exception as e:
            print(f"Error processing order: {e}")

except KeyboardInterrupt:
    print("\nShutting down order tracker...")
finally:
    consumer.close()
    