from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="Job Aggregator API")

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Job Aggregator API is running 🚀"}
