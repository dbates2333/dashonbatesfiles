"""
DealFlow AI — Agentic Deal Justification Platform
FastAPI backend with WebSocket support for streaming agent updates.
"""
import os
import json
import asyncio
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, SessionLocal
from routers import deals, artifacts, command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB, seed data, and run initial health scoring on startup."""
    logger.info("Starting DealFlow AI backend...")
    init_db()

    # Seed data if DB is empty
    db = SessionLocal()
    try:
        from models import Deal
        count = db.query(Deal).count()
        if count == 0:
            logger.info("Seeding database with initial data...")
            from seed_data import seed_all
            await seed_all(db)
            logger.info("Database seeded successfully.")
        else:
            logger.info(f"Database already has {count} deals, skipping seed.")
    finally:
        db.close()

    logger.info("DealFlow AI backend ready.")
    yield
    logger.info("DealFlow AI backend shutting down.")


app = FastAPI(
    title="DealFlow AI",
    description="Agentic Deal Justification Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS — allow all origins in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(deals.router, prefix="/deals", tags=["deals"])
app.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])
app.include_router(command.router, prefix="/command", tags=["command"])


# Active WebSocket connections per deal
ws_connections: dict[int, list[WebSocket]] = {}


@app.websocket("/ws/{deal_id}")
async def websocket_endpoint(websocket: WebSocket, deal_id: int):
    """WebSocket endpoint for streaming agent updates per deal."""
    await websocket.accept()

    if deal_id not in ws_connections:
        ws_connections[deal_id] = []
    ws_connections[deal_id].append(websocket)

    try:
        # Keep connection alive, receiving any client messages
        while True:
            data = await websocket.receive_text()
            # Echo back as heartbeat
            await websocket.send_text(json.dumps({"type": "heartbeat", "deal_id": deal_id}))
    except WebSocketDisconnect:
        if deal_id in ws_connections:
            ws_connections[deal_id].remove(websocket)
            if not ws_connections[deal_id]:
                del ws_connections[deal_id]


async def broadcast_to_deal(deal_id: int, message: dict):
    """Broadcast a message to all WebSocket connections for a deal."""
    if deal_id in ws_connections:
        dead = []
        for ws in ws_connections[deal_id]:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.append(ws)
        for ws in dead:
            ws_connections[deal_id].remove(ws)


# Make broadcast function available to routers
app.state.broadcast_to_deal = broadcast_to_deal


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "dealflow-ai"}
