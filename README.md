# 🎬 Movie Search API - FastAPI Project

## ⚙️ SETUP

To run the application locally:

```bash
uvicorn main:app --reload
```

Access the **Swagger UI** for interactive API docs at:

[http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)

> **Note:** Append `/docs#` to the local host URL to view the documentation.

---

## 🔌 APIs Used

### 1. **OMDB API**
- **API Key:** `95cfd56f`  
- **Base URL:** `http://www.omdbapi.com/`
- **Params:**
  - `s`: Title
  - `t`: Title
  - `Type`
  - `apikey`
- **Routes:**
  - `/omdb/movies/search`
  - `/omdb/movies/search/title`
- **Response:** JSON

---

### 2. **TMDB API**
- **API Key:** `860931e0c13124965476c60e9c1141fd`
- **Base URLs:**
  - `https://api.themoviedb.org/3/movie/`
  - `https://api.themoviedb.org/3/search/movie`
- **Params:**
  - `query`: Title
  - `api_key`
- **Routes:**
  - `/tmdb/movies/search/title`
  - `/tmdb/movies/search/id`
- **Response:** JSON

---

### 3. **Advanced Movie API (via RapidAPI)**
- **API Key:** `8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5`
- **Proxy Secret:** `4d633e10-2ff4-11ef-a338-672c018612df`
- **URL:** `/api/v1/streamitfree/genres/{genre}`
- **Params:**
  - `genre`
- **Route:**
  - `/movies/search/genre`
- **Response:** JSON

---

### 4. **Online Movie Database API (via RapidAPI)**
- **API Key:** `8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5`
- **URL:**  
  `/v2/search?searchTerm={ActorModified}&type=NAME&first=20&country=US&language=en-US`
- **Params:**
  - `Actor`: Actor Name
- **Route:**
  - `/movies/search/Actor`
- **Response:** JSON

---

## 📝 SUMMARY

- ✅ There are **7 search routes**, each representing one of the following search filters:
  - `Id`, `Title`, `Actor Name`, `Genre`, `Type`
- ✅ Default values are provided for each search parameter to simplify testing.
- ✅ **Dependency Injection** is implemented using a `Search` class for validating input parameters with **Pydantic**.
- ✅ **Error Handling** includes:
  - Catching third-party API errors
  - Validating incoming requests with clear messages
  - Returning proper HTTP status codes and descriptive error messages
- ✅ A **unit test** file is included for debugging and reliability.
- ✅ A **Request Cashe** file is included (5.min duration) for optimization and reliability