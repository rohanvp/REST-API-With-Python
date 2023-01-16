from bs4 import BeautifulSoup
import requests
import pymongo
from flask import Flask
app=Flask(__name__)


#SCRAPER
def imdb_top50():
    url="https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&ref_=adv_prv"

    html_text=requests.get(url).text

    soup=BeautifulSoup(html_text,"lxml")
    movies=soup.find_all('div',class_='lister-item mode-advanced')
    
    for movie in movies:
        #scraping data from imdb website for top50 movies
        rank=movie.find('span',class_='lister-item-index unbold text-primary').text.replace('.','')
        movie_name=movie.find('h3',class_='lister-item-header').find('a').text
        star_rating=movie.find('div',class_='inline-block ratings-imdb-rating').find('strong').text
        genre=movie.find('span',class_='genre').text.strip()
        runtime=movie.find('span',class_='runtime').text.replace(' ','')
        ' '.join(genre.split())
        insert_data(rank,movie_name,star_rating,genre,runtime)
        
        
        
def insert_data(rank,movie_name,star_rating,genre,runtime):
    #mongodb entry
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['imdb']#db name
    mycol = mydb["top50"]#collection name
    mydict = { "rank":rank,"movie_name": movie_name,"star_rating": star_rating,"genre": genre,"runtime": runtime }
    mycol.insert_one(mydict)


#REST API FROM OBTAINED DATA
@app.route('/imdb/top50/')
def get_all_movies():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['imdb']
    mycol = mydb["top50"]
    result=mycol.find()
    final=[]
    for x in result:
        temp={x['rank']:{'rank':x['rank'],'name':x['movie_name'],'rating':x['star_rating'],'genre':x['genre'],'runtime':x['runtime']}}
        final.append(temp)
    return final

@app.route('/imdb/top50/<rank>')
def get_movie_with_rank(rank):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['imdb']
    mycol = mydb["top50"]
    result=mycol.find({"rank":rank })
    final=[]
    for x in result:
        temp={x['rank']:{'rank':x['rank'],'name':x['movie_name'],'rating':x['star_rating'],'genre':x['genre'],'runtime':x['runtime']}}
        final.append(temp)
    return final


#UNCOMMENT BELOW FOR SPECIFIC TASK

#WHILE RUNNING FOR FIRST TIME. COMMENT FOR RUNNING AFTER MONGODB ENTRIES ARE MADE
# imdb_top50()