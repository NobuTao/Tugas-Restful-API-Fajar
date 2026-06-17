from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author: str
    is_read: bool = False