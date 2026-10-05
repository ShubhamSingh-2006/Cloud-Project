import os
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI

INSTANCE_ID = os.getenv("INSTANCE_ID", "instance-local")

app = FastAPI(
    title="Load-Balanced Multi-Instance App",
    version="1.0.0",
    description="A simple FastAPI service used to demonstrate horizontal scaling and load balancing.",
)


@app.get("/")
def read_root():
    return {
        "message": "Load-balanced application is running!",
        "instance_id": INSTANCE_ID,
        "try": "/health or /instance",
    }


@app.get("/instance")
def get_instance():
    return {
        "instance_id": INSTANCE_ID,
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "instance_id": INSTANCE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
