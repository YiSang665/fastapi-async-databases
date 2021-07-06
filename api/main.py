from fastapi import FastAPI
from .database import metadata, db, engine
from . import articles, users, auth

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(articles.router)
app.include_router(users.router)
app.include_router(auth.router)