
from fastapi import FastAPI
from .routes.route import router
from .auth import router as auth_router

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)