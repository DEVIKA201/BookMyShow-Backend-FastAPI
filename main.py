from fastapi import FastAPI
from app.routes import artist_routes,booking_routes,movie_routes,show_routes,user_routes,venue_routes

from app.config.postgres_config import engine
from app.models.postgres import Base

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Book My Show",
    version="1.0.0"
)

app.include_router(artist_routes.artist_router)
app.include_router(movie_routes.movie_router)
app.include_router(venue_routes.venue_router)
app.include_router(venue_routes.location_router)
app.include_router(user_routes.user_router)
app.include_router(show_routes.show_router)
app.include_router(venue_routes.screen_router)