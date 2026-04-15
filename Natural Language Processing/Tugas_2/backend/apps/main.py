from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from services.service_tfidf import service_tfidf
from model.QueryModel import QueryModel , TypeMethodEnum
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Generate vectorizenya
    print("Start the service")
    print("Membuat vectorize")
    service = service_tfidf
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/", response_class=HTMLResponse)
async def main(request : QueryModel):
    
    if request.type == TypeMethodEnum.COSINE:
        return service_tfidf.getScoreCosineSimiliarity(request.query)
    
    if request.type == TypeMethodEnum.TFIDF:
        return service_tfidf.getScoreTFIDF(request.query)