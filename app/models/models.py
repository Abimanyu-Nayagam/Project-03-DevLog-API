from pydantic import BaseModel
from datetime import date

class ExportEntryRequest(BaseModel):
    id: int

class ExportSnippetRequest(BaseModel):
    id: int
