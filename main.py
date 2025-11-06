from fastapi import FastAPI
from app.routes import artist_routes, booking_routes ,movie_routes, show_routes,user_routes,venue_routes, seatlayout_routes
import asyncio
from app.tasks.auto_unlock import auto_unlock_expired_seats
from app.config.postgres_config import engine
from app.models.postgres import Base

import warnings
warnings.filterwarnings(
    "ignore",
    message="Valid config keys have changed in V2:",
    category=UserWarning
)

from contextlib import asynccontextmanager


Base.metadata.create_all(bind = engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    unlock_task = asyncio.create_task(auto_unlock_expired_seats())
    
    yield  

    # Shutdown
    unlock_task.cancel()

app = FastAPI(
    title="Book My Show",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(artist_routes.artist_router)
app.include_router(movie_routes.movie_router)
app.include_router(venue_routes.venue_router)
app.include_router(venue_routes.location_router)
app.include_router(user_routes.user_router)
app.include_router(show_routes.show_router)
app.include_router(venue_routes.screen_router)
app.include_router(booking_routes.booking_router)
app.include_router(seatlayout_routes.seatlayout_router)