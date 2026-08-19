from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Sentinel", lifespan=lifespan)


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Sentinel API",
    )



@app.get("/health/")
async def get_health():
    return {"status": "active"}
