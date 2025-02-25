from fastapi import FastAPI, WebSocket
from core.connections import Connection
from apps.users.routers import router as users_router
from apps.categories.routers import router as categories_router
from apps.orders.routers import router as orders_router
from apps.products.routers import router as products_router
from fastapi import WebSocketDisconnect
from typing import List


# Define an asynchronous lifespan function for the FastAPI app
async def lifespan(app: FastAPI):
    # Initialize a connection and store it in the app's state
    app.state.connection = Connection()
    yield
    # Close the connection when the app shuts down
    await app.state.connection.close()

# Create a FastAPI app instance with metadata and lifespan
app = FastAPI(
    title="Caffelito API",
    description="API for the Caffelito Coffee Shop",
    version="0.1.0",
    lifespan=lifespan,
)

# Define a root endpoint that returns a welcome message
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Caffelito Coffee Shop API"}

# Define a health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Class to manage WebSocket connections
class ConnectionManager:
    def __init__(self):
        # List to keep track of active WebSocket connections
        self.active_connections: List[WebSocket] = []

    # Method to accept and store a new WebSocket connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Method to remove a WebSocket connection
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Method to send a personal message to a specific WebSocket
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # Method to broadcast a message to all active WebSocket connections
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Instantiate the connection manager
manager = ConnectionManager()

# WebSocket endpoint for chat functionality
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    # Connect the WebSocket
    await manager.connect(websocket)
    try:
        while True:
            # Receive a message from the WebSocket
            data = await websocket.receive_text()
            # Broadcast the received message to all connections
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        # Handle disconnection
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")

# Include routers for different app modules
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(categories_router, tags=["categories"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(products_router, prefix="/products", tags=["products"])

