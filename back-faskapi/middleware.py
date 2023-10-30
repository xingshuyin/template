from main import app
from fastapi import Request


@app.middleware("http")
async def permission(request: Request, call_next):
    user = request.cookies.get('token')
