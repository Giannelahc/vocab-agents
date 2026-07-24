from fastapi import FastAPI
from api import auth_controller
from database import init_db

app = FastAPI(title="Vocabulary API")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth_controller.router, prefix="/vocan-agent/auth", tags=["Auth"])