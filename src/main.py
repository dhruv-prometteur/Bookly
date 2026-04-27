from fastapi import FastAPI
from src.books.routers import book_router

from contextlib import asynccontextmanager
from src.db.database import init_db
from src.auth.routes import user_router
from src.review.routers import review_router
from .middleware import register_middleware
from .error import register_all_errors



@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting up the application...")
    await init_db()
    yield
    print("shutting down the application...")

version="v1"

app=FastAPI(
    title="Bookly",
    description="A Book Management System",
    version=version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact={
        "email":"dhruvpatel2581@gmail.com"
    },
    lifespan=lifespan
    )


register_all_errors(app)
register_middleware(app)
app.include_router(book_router,prefix=f"/api/{version}/books",tags=["Books"])
app.include_router(user_router,prefix=f"/api/{version}/user",tags=["user"])
app.include_router(review_router,prefix=f"/api/{version}/review",tags=["Reviews"])

