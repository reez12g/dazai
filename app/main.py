from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp import NLP
from task import Task
from cliche import Cliche
import requests
import json
from pydantic import BaseModel

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
    payload = json.dump({
        "text": cliche.cliche
    })
    response = requests.post(
        response_url,
        payload
    )

@app.post("/predictive_sentences/")
def predictive_sentences(sentence_material: SentenceMaterial):
    payload = json.dump({
        "text": nlp.predictive_sentences(text=sentence_material.text),
        "response_type": "in_channel"
    })
    response = requests.post(
        sentence_material.response_url,
        payload
    )
