    SETUP
        -to run app >>uvicorn main:app --reload
        -SWAGGER UI PORT: http://127.0.0.1:8000/docs#/
        -ADD 'docs#' at the end of the host
APIs used is :
1-OMDB API
    apiKey:
        "95cfd56f"
    Url:
        "http://www.omdbapi.com/"
    params:
        "s"  #(title),
        "Type",
        "apikey",
        "t"  #(title)
    route:
        "/omdb/movies/search",
        "/omdb/movies/search/title"
    response:
        JSON
2-TMDB API
    apiKey:
        "860931e0c13124965476c60e9c1141fd"
    Url: 
        "https://api.themoviedb.org/3/movie/",
        "https://api.themoviedb.org/3/search/movie"
    params:
        "query"  #(title),
        "api_key",
    route:
        "/tmdb/movies/search/title",
        "/tmdb/movies/search/id"
    response:
        JSON
3-advance-movie-api.p.rapidapi.com
    apiKey:
        "8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5"
    Proxy-Secret:
        "4d633e10-2ff4-11ef-a338-672c018612df"
    Url:
        f"/api/v1/streamitfree/genres/{genre}"
    params:
        genre
    route:
        "/movies/search/genre"
    response:
        JSON
4-online-movie-database.p.rapidapi.com
    apiKey:
        "8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5"
    Url:
        f"/v2/search?searchTerm={ActorModified}&type=NAME&first=20&country=US&language=en-US"
    params:
        Actor (Actor_name)
    route:
        "/movies/search/Actor"
    response:
        JSON

    SUMMARY

        -there are 7 search routes each represent on of the required search filter 
        (Id,Title,Actorname,Genre,Type).
        -Each given a default value to improve testing.
        -I used search class to represent the input parameter for validating variable using pydantic and for dependency injection
        -For error handling i Handled third-party API errors, Validated incoming requests with clear error messages and Returned proper HTTP status codes and descriptive messages. 
        -I added unit test file for debbuging.
        
