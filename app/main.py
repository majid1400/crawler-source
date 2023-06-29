import uvicorn as uvicorn
from fastapi import FastAPI

from app.resource.apiv1.user import router

app = FastAPI(version="1.0")
app.include_router(router, prefix="/platforms")

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
