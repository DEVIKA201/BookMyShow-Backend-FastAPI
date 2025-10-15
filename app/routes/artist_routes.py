from fastapi import APIRouter

from app.schemas.artist_schema import Artist, DeleteArtist,UpdateArtist
from app.services.artist_service import get_artists, get_artist_by_id,create_artist,update_artist, soft_delete_artist

artist_router = APIRouter(prefix="/artists",tags=["Artists"])

#Create new artist
@artist_router.post("/",response_model=Artist)
async def create_new_artist(artist: Artist):
    return await create_artist(artist)

#Fetch all artists
@artist_router.get("/",response_model=list[Artist])
async def read_all_artist():
    return await get_artists()

#Fetch an artist
@artist_router.get("/{artist_id}", response_model=Artist)
async def read_artist(artist_id: str):
    return await get_artist_by_id(artist_id)

#Update artist details
@artist_router.put("/{artist_id}",response_model=UpdateArtist)
async def update_artist_by_id(artist_id:str, artist: UpdateArtist):
    return await update_artist(artist_id,artist)

#Soft delete artist
@artist_router.delete("/{artist_id}", response_model=DeleteArtist)
async def delete_artist(artist_id:str):
    return await soft_delete_artist(artist_id)
    