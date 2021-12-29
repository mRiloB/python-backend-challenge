from fastapi import FastAPI
from controllers.articles import controller_getArticles


app = FastAPI()


@app.get("/")
async def root():
    return {
        "Status": 200,
        "Message": "Back-end Challenge 2021 🏅 - Space Flight News"
    }


@app.get("/articles")
async def get_articles(limit: int = 10):
    ret = controller_getArticles(limit=limit)
    return ret


@app.get("/articles/{article_id}")
async def get_article_by_id(article_id: int):
    ret = controller_getArticles(id=article_id)
    return ret
