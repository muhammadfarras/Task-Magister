from pydantic import BaseModel
from enum import Enum

class TypeMethodEnum(Enum):
    COSINE = 'COSINE'
    TFIDF = 'TFIDF'

class QueryModel(BaseModel):
    query : str
    type : TypeMethodEnum



