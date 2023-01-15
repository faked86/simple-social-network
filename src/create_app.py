from fastapi import FastAPI

from src.api.auth.views import auth_router
from src.api.posts.views import posts_router


app = FastAPI(
    title="Simple social network",
)


def create_app():
    app.include_router(auth_router)
    app.include_router(posts_router)
    return app
