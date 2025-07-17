import string
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel, Field
import httpx
import http.client
import json
from aiocache import cached, Cache
    

#uvicorn main:app --reload
app = FastAPI()

class Movies(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Movie title to search for")
    type: str = Field(default="movie", pattern="^(movie|series|episode)$", description="Type of media")
    title: str = Query(..., min_length=1),
    media_type: str = Query("movie", pattern="^(movie|series|episode)$")

#if type not in ["movie", "series", "episode"]:
        #raise HTTPException(status_code=400, detail="Type must be 'movie', 'series', or 'episode'")


OMDB_API_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = "95cfd56f"
TMDB_API_URL_id = "https://api.themoviedb.org/3/movie/"
TMDB_API_URL_title = "https://api.themoviedb.org/3/search/movie"
TMDB_API_KEY = "860931e0c13124965476c60e9c1141fd"

def get_omdb_key() -> str:
    return "95cfd56f"

def get_tmdb_key() -> str:
    return "860931e0c13124965476c60e9c1141fd"


@cached(ttl=300, cache=Cache.MEMORY)
async def get_response(params: dict = None):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OMDB_API_URL, params=params)
            response.raise_for_status()
            data = response.json()        
            if data.get("Response") == "False":
                raise HTTPException(status_code=404, detail=data.get("Error", "Movie not found"))
        return data    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="OMDb API timeout.")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"OMDb API error: {exc.response.text}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="OMDb API unreachable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
async def get_response_id(movie_id: str = "725201",params: dict = None):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(TMDB_API_URL_id + movie_id, params=params)
            response.raise_for_status()
            data = response.json()        
            if data.get("Response") == "False":
              raise HTTPException(status_code=404, detail=data.get("Error", "Movie not found"))
            
        return data
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="TMDb API timeout.")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"TMDb API error: {exc.response.text}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="TMDb API unreachable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def get_response_title(params: dict = None):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(TMDB_API_URL_title, params=params)
            response.raise_for_status()
            data = response.json()            
            if data.get("Response") == "False":
                raise HTTPException(status_code=404, detail=data.get("Error", "Movie not found"))
            
        return data
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="TMDb API timeout.")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"TMDb API error: {exc.response.text}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="TMDb API unreachable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@cached(ttl=300, cache=Cache.MEMORY)
async def get_response_genre(genre: string):
    conn = http.client.HTTPSConnection("advance-movie-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5",
        'x-rapidapi-host': "advance-movie-api.p.rapidapi.com",
        'X-RapidAPI-Proxy-Secret': "4d633e10-2ff4-11ef-a338-672c018612df"
    }

    conn.request("GET", f"/api/v1/streamitfree/genres/{genre}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    if data.get("Response") == "False":
            raise HTTPException(status_code=404, detail=data.get("Error", "Movie not found"))
    
    json_data = json.loads(data.decode("utf-8"))
    return json_data

@cached(ttl=300, cache=Cache.MEMORY)
async def get_response_Actor(Actor: str):

    conn = http.client.HTTPSConnection("online-movie-database.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5",
        'x-rapidapi-host': "online-movie-database.p.rapidapi.com"
    }
    ActorModified = Actor.replace(" ","+")
    conn.request("GET", f"/v2/search?searchTerm={ActorModified}&type=NAME&first=20&country=US&language=en-US", headers=headers)

    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    return json_data

@app.get("/omdb/movies/search")
async def search_movies(title: str = "lucy",type: str = "movie"):
    params = {
        "s": title.strip(),
        "Type": type,
        "apikey":  get_omdb_key()
    }
    o = await get_response(params)
    return o

@app.get("/omdb/movies/search/title")
async def search_movies_by_title(title: str = "lucy"):
    params = {
        "t": title.strip(),
        "apikey": get_omdb_key()
    }
    o = await get_response(params)
    return o

@app.get("/omdb/movies/search/id")
async def search_movies_by_id(Imdb_id: str ="tt0147746"):
    params = {
        "i": Imdb_id,
        "apikey": get_omdb_key()
    }
    o = await get_response(params)
    return o

@app.get("/tmdb/movies/search/title")
async def search_movies_by_title(title: str = "lucy"):
    params = {
        "query": title.strip(),
        "api_key": get_tmdb_key()
    }
    o = await get_response_title(params)
    return o
        

@app.get("/tmdb/movies/search/id")
async def search_movies_by_id(Imdb_id: str ="725201"):
    params = {
        "api_key": get_tmdb_key()         
    }
    o = await get_response_id(params)
    return o

@app.get("/movies/search/genre")
async def search_movies_by_genre(genre: str = "Action"):
    o = await get_response_genre(genre)
    return o

@app.get("/movies/search/Actor")
async def search_movies_by_Actor(Actor: str = "tom cruise"):
    o = await get_response_Actor(Actor)
    return o



#tom%20cruise