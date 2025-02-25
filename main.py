from fastapi import FastAPI, WebSocket
from core.connections import Connection
from apps.users.routers import router as users_router
from apps.categories.routers import router as categories_router
from apps.orders.routers import router as orders_router
from apps.products.routers import router as products_router
from fastapi import WebSocketDisconnect
from typing import List


async def lifespan(app: FastAPI):
    app.state.connection = Connection()
    yield
    await app.state.connection.close()

app = FastAPI(
    title="Caffelito API",
    description="API for the Caffelito Coffee Shop",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Caffelito Coffee Shop API"}

@app.get("/health")
async def health():
    return {"status": "ok"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(categories_router, tags=["categories"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(products_router, prefix="/products", tags=["products"])

