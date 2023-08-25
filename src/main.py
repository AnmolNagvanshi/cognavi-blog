from fastapi import FastAPI
from src.router import api_router
import uvicorn


app = FastAPI()

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0",
                port=8000, log_level="info", reload=True)

