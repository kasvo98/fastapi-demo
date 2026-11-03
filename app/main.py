from fastapi import FastAPI, Depends
from app.routers.rooms import router as rooms_router
from app.routers.bookings import router as bookings_router
from app.settings import Settings, get_settings
from app.database import init_db


init_db()
app = FastAPI()
app.include_router(rooms_router, prefix="/api/rooms")
app.include_router(bookings_router, prefix="/api/rooms")


@app.get("/info")
def info(settings: Settings = Depends(get_settings)):
    return {"app": settings.app_name}
