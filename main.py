from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(
    title="Articles API",
    description="CRUD operations for a articles management application",
    version="1.0.0"
)

articles_database:List[dict] = [
    {'id':1, 'title':'Python 3 Basics', 'description':'Learn the basics of python 3', 'author':'Gaideh Brian'},
    {'id':2, 'title':'Interview preparation','description':'Get tips on how to answer interview questions'}
]

# Article Model
class Article(BaseModel):
    title: str 
    description: str
    author: str


@app.get('/')
def home():
    return {"message":"Hello world"}

# GET
@app.get('/articles',status_code=200, tags=["Article"], summary="Get all the articles", response_description="All articles")
async def get_articles():
    return {"articles":articles_database}

# GET {ID}
@app.get('/articles/{article_id}',status_code=200, tags=["Article"], summary="Get an article by ID", response_description="An article")
async def get_article(article_id:int):
    article = next(filter(lambda art: art['id']== article_id, articles_database), None)
    if not article:
        raise HTTPException(status_code=404, detail='article not found')
    return article

# POST
@app.post('/articles',status_code=201, tags=["Article"], summary="Create an article", response_description="The created article")
async def create_article(article: Article):
    the_article = article.dict()
    the_article['id'] = len(articles_database)+1
    articles_database.append(the_article)
    return {"articles":articles_database}


# PUT
@app.put('/articles/{article_id}',status_code=200, tags=["Article"], summary="Update and article by ID")
async def update_article(article_id:int, new_article:Article):
    # find the article by id
    article = next(filter(lambda art: art['id']== article_id, articles_database), None)
    if not article:
        raise HTTPException(status_code=404, detail='article not found')

    article['title'] = new_article.title
    article['description'] = new_article.description
    article['author'] = new_article.author

    return article



# DELETE
@app.delete('/articles/{article_id}',status_code=200, tags=["Article"],summary="Delete an article by ID")
async def delete_article(article_id:int):
    # locate the article
    article = next(filter(lambda art: art['id']== article_id, articles_database), None)
    if not article:
        raise HTTPException(status_code=404, detail='article not found')
    
    # remove the article from the list
    articles_database.remove(article)
    return {
        'articles':articles_database
    }
    



