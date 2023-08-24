from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

from router import router
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0",
                port=8000, log_level="info", reload=True)
