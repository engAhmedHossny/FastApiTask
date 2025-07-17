from fastapi.testclient import TestClient
from main import app, get_omdb_key, get_tmdb_key

def override_omdb_key():
    return "test_omdb_api_key"

def override_tmdb_key():
    return "test_tmdb_api_key"

app.dependency_overrides[get_omdb_key] = override_omdb_key
app.dependency_overrides[get_tmdb_key] = override_tmdb_key

client = TestClient(app)


def test_omdb_search_movies(monkeypatch):

    def mock_get_response(params):
        return {"Search": [{"Title": "Lucy", "Year": "2014"}]}

    monkeypatch.setattr("main.get_response", mock_get_response)

    response = client.get("/omdb/movies/search", params={"title": "lucy", "type": "movie"})
    assert response.status_code == 200
    assert response.json() == {"Search": [{"Title": "Lucy", "Year": "2014"}]}

def test_omdb_search_by_id(monkeypatch):
    def mock_get_response(params):
        return {"Title": "Fight Club", "Year": "1999"}

    monkeypatch.setattr("main.get_response", mock_get_response)

    response = client.get("/omdb/movies/search/id", params={"Imdb_id": "tt0137523"})
    assert response.status_code == 200
    assert response.json()["Title"] == "Fight Club"

def test_tmdb_search_by_title(monkeypatch):
    def mock_get_response_title(params):
        return {"results": [{"title": "Lucy", "id": 240832}]}

    monkeypatch.setattr("main.get_response_title", mock_get_response_title)

    response = client.get("/tmdb/movies/search/title", params={"title": "lucy"})
    assert response.status_code == 200
    assert response.json()["results"][0]["title"] == "Lucy"

def test_tmdb_search_by_id(monkeypatch):
    def mock_get_response_id(movie_id, params):
        return {"id": 240832, "title": "Lucy"}

    monkeypatch.setattr("main.get_response_id", mock_get_response_id)

    response = client.get("/tmdb/movies/search/id", params={"Imdb_id": "240832"})
    assert response.status_code == 200
    assert response.json()["title"] == "Lucy"
