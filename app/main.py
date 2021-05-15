from fastapi import FastAPI
from app.routes.linebot import router as linebot_router

app = FastAPI()
app.include_router(linebot_router, prefix="/api")


@app.get("/")
def health_check():
    return {"Hello": "hello"}
