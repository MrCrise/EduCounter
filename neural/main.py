from fastapi import FastAPI
from sse_api import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="EduCounter AI-Detection Microservice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Type"],
    allow_credentials=True,
)

app.include_router(router, prefix="/api")


@app.get("/routes")
def list_routes():
    return [{"path": r.path, "methods": list(r.methods)} for r in app.router.routes]
