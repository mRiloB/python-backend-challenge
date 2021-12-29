import requests
import json
from models.article import Article
from db.postgres import Database


def fetch(url: str):
    response = requests.get(url)
    return json.loads(response.content)


def get_articles_counter() -> int:
    db = Database()
    articles_counter = fetch(
        "https://api.spaceflightnewsapi.net/v3/articles/count")
    articles_db = db.getCounter()
    aux = db.updateCounter((articles_counter,))
    print(aux)
    db.close()
    return articles_counter - articles_db


def insert_articles():
    db = Database()
    amount = get_articles_counter()
    print(f"\n!!! This script will add {amount} new articles !!!\n")
    articles = fetch(
        f"https://api.spaceflightnewsapi.net/v3/articles?_limit={amount}")
    for row in articles:
        article = Article(**row)
        try:
            # insert into articles
            sql = """
                    INSERT INTO articles
                    ( id, featured, title, url, "imageUrl", "newsSite", summary, "publishedAt", "updatedAt" )
                    VALUES
                    ( %s, %s, %s, %s, %s, %s, %s, %s, NOW() )
                    RETURNING id;
                """
            db.execute(sql, (
                article.id,
                article.featured,
                article.title,
                article.url,
                article.imageUrl,
                article.newsSite,
                article.summary,
                article.publishedAt
            ))

            # insert into launches
            if len(article.launches) > 0:
                sql = """
                        INSERT INTO launches
                        ( id, provider, article_id )
                        VALUES
                        ( %s, %s, %s )
                        RETURNING id;
                    """
                for launch in article.launches:
                    db.execute(sql, (launch.id, launch.provider, article.id))

            # insert into events
            if len(article.events) > 0:
                sql = """
                        INSERT INTO events
                        ( id, provider, article_id )
                        VALUES
                        ( %s, %s, %s )
                        RETURNING id;
                    """
                for event in article.events:
                    db.execute(sql, (event.id, event.provider, article.id))

        except Exception as error:
            print(error)

        print(
            f"Article with id {article.id} was inserted with {len(article.launches)} launches and {len(article.events)} events!")

    db.close()


if __name__ == "__main__":
    insert_articles()
