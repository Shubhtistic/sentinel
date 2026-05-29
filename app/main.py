from fastapi import FastAPI

app = FastAPI(title="Sentinel")


@app.get("/health/")
async def get_health():
    return {"status": "active"}
