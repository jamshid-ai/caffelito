from fastapi import FastAPI
from core.connections import Connection
from apps.users.routers import router as users_router
from apps.categories.routers import router as categories_router

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

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(categories_router, tags=["categories"])
