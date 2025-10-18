from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List, Dict, Any, Iterator
import json
import threading
from queue import Queue, Empty
from confluent_kafka import Consumer
import os

from services.shared.models import MENU_ITEMS

app = FastAPI(title="Admin Service", description="Admin-facing metrics and events", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory metrics
metrics = {
    "orders_total": 0,
    "revenue_total": 0.0,
}

# Kafka consumer in background thread, pushing messages to a queue
messages: "Queue[Dict[str, Any]]" = Queue()


def start_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
            "group.id": "admin-metrics",
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe(["burger-orders"]) 
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        try:
            data = json.loads(msg.value().decode("utf-8"))
            messages.put(data)
            # Update metrics
            metrics["orders_total"] += 1
            metrics["revenue_total"] += float(data.get("total_amount", 0.0))
        except Exception:
            continue


consumer_thread = threading.Thread(target=start_consumer, daemon=True)
consumer_thread.start()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics():
    return metrics


@app.get("/events")
async def sse_events():
    def event_stream() -> Iterator[bytes]:
        while True:
            try:
                evt = messages.get(timeout=5)
                yield f"data: {json.dumps(evt)}\n\n".encode("utf-8")
            except Empty:
                # keep connection alive
                yield b": keep-alive\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

# serve static dashboard
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "static"), html=True), name="static")
