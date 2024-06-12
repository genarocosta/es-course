import csv, re, wget, os
from collections import deque
from elasticsearch import helpers, Elasticsearch
if not os.path.exists('movies.csv'):
    wget.download('https://raw.githubusercontent.com/jeknov/movieRec/master/movies.csv')
def readMovies():
    csvfile = open('movies.csv', 'r')
    reader = csv.DictReader( csvfile )
    for movie in reader:
        title = re.sub(" \\(.*\\)$", "", re.sub('"','', movie['title'])) 
        year = movie['title'][-5:-1]
        if (not year.isdigit()): year = "2016"
        movie['genres'] = movie['genres'].split('|')
        movie['year'] = year
        movie['title'] = title
        yield movie

es = Elasticsearch('http://localhost:9200')
es.indices.delete(index="movies",ignore=404)
deque(helpers.parallel_bulk(es,readMovies(),index="movies"), maxlen=0)
es.indices.refresh()
