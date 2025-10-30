from pydantic import BaseModel
from datetime import date

class CreateSnippetRequest(BaseModel):
    title: str
    language: str
    snippet: str
    tags: str | None = None

class CreateEntryRequest(BaseModel):
    title: str
    content: str
    tags: str | None = None

class UpdateSnippetRequest(BaseModel):
    id: int
    title: str | None = None
    language: str | None = None
    snippet: str | None = None
    tags: str | None = None

class UpdateEntryRequest(BaseModel):
    id: int
    title: str | None = None
    content: str | None = None
    tags: str | None = None