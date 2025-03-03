from fastapi import FastAPI
from app.api import scenarios

app = FastAPI()

app.include_router(scenarios.router, prefix="/sandbox", tags=["sandbox"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)