from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.posts.router import router as posts_router
from app.users.router import router as users_router
from app.files.router import router as files_router


app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(files_router)


@app.get('/')
async def main_page():
    return {'msg': 'ok'}
