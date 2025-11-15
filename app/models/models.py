from pydantic import BaseModel, ConfigDict
from datetime import date

class CreateSnippetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    language: str
    snippet: str
    description: str
    tags: str | None = None

class CreateEntryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    content: str
    tags: str | None = None

class UpdateSnippetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str | None = None
    language: str | None = None
    snippet: str | None = None
    tags: str | None = None

class UpdateEntryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str | None = None
    content: str | None = None
    tags: str | None = None

class CreateUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str
    username: str
    password: str