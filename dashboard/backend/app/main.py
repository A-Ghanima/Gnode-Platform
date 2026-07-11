from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, containers, metrics

app = FastAPI(
    title="Gnode Dashboard API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(containers.router, prefix="/api/v1/containers", tags=["containers"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])

@app.get("/health")
async def health():
    return {"status": "ok"}
