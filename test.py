
import http.client

conn = http.client.HTTPSConnection("imdb-movies-shows-persons-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "8c0dbcb743msh6942d95b04d072fp130eddjsn887f0ca485d5",
    'x-rapidapi-host': "imdb-movies-shows-persons-api.p.rapidapi.com"
}

conn.request("GET", "/search/persons?query=Dwayne+johnson", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))