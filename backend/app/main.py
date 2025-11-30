import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# --- 1. PATH SETUP (Run from anywhere) ---
# This block ensures that 'from app...' imports work regardless of
# which folder you run this script from.
# It finds the parent of the 'app' folder (the backend root) and adds it to sys.path.

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from app.api.routers import places, search  # Import the modules
from app.models import get_config
from app.services.database import DatabaseService


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    # Initialize DB on startup
    db_service = DatabaseService(config)
    SQLModel.metadata.create_all(db_service.engine)
    yield


# 2. Define Middleware Configuration explicitly
# This satisfies the type checker because Middleware is a typed wrapper
middleware = [
    Middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]
app = FastAPI(title="Travel Planner API", lifespan=lifespan, middleware=middleware)


# Register the split routers
app.include_router(places.router)
app.include_router(search.router)

if __name__ == "__main__":
    file_path = Path(__file__).resolve()
    backend_root = file_path.parent.parent
    # This allows you to run: 'uv run app/main.py'
    # reload=True requires the import string "app.main:app"
    # reload_dirs ensures it watches the correct folder for changes
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_root / "app")],
    )
