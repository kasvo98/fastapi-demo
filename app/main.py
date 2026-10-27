from fastapi import FastAPI, Depends
from .routers.rooms import router as rooms_router
from .settings import Settings, get_settings



app = FastAPI()
app.include_router(rooms_router, prefix="/api/rooms")


@app.get("/info")
def info(settings: Settings = Depends(get_settings)):
    return {"app": settings.app_name}
