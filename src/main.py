from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.shared.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # import every model module so the SQLModel registry is fully populated
    import src.alerts.models  # noqa: F401
    import src.auth.models  # noqa: F401
    import src.monitors.models  # noqa: F401

    await init_db()
    yield


app = FastAPI(title="Sentinel", lifespan=lifespan)

# TODO: incomplete — no domain routers registered yet (auth, monitors, alerts are scaffolds)


@app.get("/health/")
async def get_health():
    return {"status": "active"}
