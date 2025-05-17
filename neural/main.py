from fastapi import FastAPI
from sse_api import router


app = FastAPI(
    title="EduCounter AI-Detection Microservice",
    version="1.0.0"
)

app.include_router(router, prefix="/api")
