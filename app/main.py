from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from nlp import NLP
from task import Task
from cliche import Cliche
import requests
import json

class SentenceMaterial(BaseModel):
    text: str
    response_url: str

app = FastAPI()
nlp = NLP()
task = Task()
cliche = Cliche()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predictive_sentences_task/")
def predictive_sentences_task(text: str = Form(...), response_url: str = Form(...)):
    task.create_task(text=text, response_url=response_url)
    return JSONResponse(content={"response_type": "in_channel", "text": cliche.cliche})

@app.post("/predictive_sentences/")
def predictive_sentences(sentence_material: SentenceMaterial):
    payload = json.dumps({
        "text": nlp.predictive_sentences(text=sentence_material.text),
        "response_type": "in_channel"
    })
    print(sentence_material.text)
    print(payload)
    requests.post(
        sentence_material.response_url,
        payload
    )
