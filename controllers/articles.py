from db.postgres import Database
from models.article import ArticleByTuple, LaunchesEvents
from typing import Optional

def controller_getArticles(id: Optional[int] = 0, limit: Optional[int] = 0):
    ret = None
    db = Database()
    sql = """
        SELECT
            id,
            featured,
            title,
            url,
            "imageUrl",
            "newsSite",
            summary,
            "publishedAt",
            "updatedAt"
        FROM articles
    """

    # get all articles
    if id == 0:
        ret = []
        sql = sql + "ORDER BY id LIMIT %s;"
        articles = db.execute(sql, (limit,), True)
        for row in articles:
            article = ArticleByTuple(row)
            article.launches = getLaunchesEvents('launches', article.id, db)
            article.events = getLaunchesEvents('events', article.id, db)

            ret.append({
                "id": article.id,
                "featured": article.featured,
                "title": article.title,
                "url": article.url,
                "imageUrl": article.imageUrl,
                "newsSite": article.newsSite,
                "summary": article.summary,
                "publishedAt": article.publishedAt,
                "updatedAt": article.updatedAt,
                "launches": article.launches,
                "events": article.events
            })
    # END

    # get article by id
    else:
        sql = sql + "WHERE id = %s;"
        article = db.execute(sql, (id,))
        article = ArticleByTuple(article)
        article.launches = getLaunchesEvents('launches', article.id, db)
        article.events = getLaunchesEvents('events', article.id, db)
        ret = {
            "id": article.id,
            "featured": article.featured,
            "title": article.title,
            "url": article.url,
            "imageUrl": article.imageUrl,
            "newsSite": article.newsSite,
            "summary": article.summary,
            "publishedAt": article.publishedAt,
            "updatedAt": article.updatedAt,
            "launches": article.launches,
            "events": article.events
        }
    # END

    db.close()
    return ret
        
def getLaunchesEvents(table: str, id: int, db: Database):
    ret = []
    sql = f"SELECT id, provider FROM {table} WHERE article_id = %s;"
    rows = db.execute(sql, (id,), True)
    for row in rows:
        launchEvent = LaunchesEvents(id=row[0], provider=row[1])
        ret.append(launchEvent)
    return ret
    














