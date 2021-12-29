from typing import List, Optional
from pydantic import BaseModel

class LaunchesEvents(BaseModel):
    id: str
    provider: Optional[str]

class Article(BaseModel):
    id: int
    featured: bool = False
    title: str
    url: str
    imageUrl: str
    newsSite: str
    summary: str
    publishedAt: str
    updatedAt: Optional[str]
    launches: Optional[List[LaunchesEvents]]
    events: Optional[List[LaunchesEvents]]

def ArticleByTuple(data: tuple):
    return Article(
            id=data[0],
            featured=data[1],
            title=data[2],
            url=data[3],
            imageUrl=data[4],
            newsSite=data[5],
            summary=data[6],
            publishedAt=data[7],
            updatedAt=data[8],
            launches=[],
            events=[]
        )