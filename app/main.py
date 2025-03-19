import json
import logging
from typing import Dict, Any

import requests
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl

# Use absolute imports for local modules
from app.nlp import NLP
from app.task import Task
from app.cliche import Cliche

# Configure logging
logger = logging.getLogger(__name__)

# Define data models
class SentenceMaterial(BaseModel):
    """Data model for sentence generation request."""
    text: str
    response_url: HttpUrl

class ResponseMessage(BaseModel):
    """Data model for API responses."""
    text: str

# Initialize FastAPI app
app = FastAPI(
    title="Dazai API",
    description="API for predictive text generation using GPT-2",
    version="1.0.0"
)

# Initialize services
nlp = NLP()
task = Task()
cliche = Cliche()

# Configure CORS
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

@app.get("/", response_model=ResponseMessage, tags=["General"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint that returns a random cliche.

    Returns:
        A dictionary with a random cliche message
    """
    try:
        return {"text": cliche.cliche()}
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.post("/predictive_sentences_task/", response_model=ResponseMessage, tags=["Tasks"])
async def predictive_sentences_task(text: str = Form(...), response_url: str = Form(...)) -> JSONResponse:
    """
    Create a Cloud Task for asynchronous sentence generation.

    Args:
        text: The input text to generate from
        response_url: The URL to send the generated text to

    Returns:
        A JSON response with a random cliche message
    """
    try:
        task.create_task(text=text, response_url=response_url)
        return JSONResponse(content={"text": cliche.cliche()})
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@app.post("/predictive_sentences/", status_code=status.HTTP_202_ACCEPTED, tags=["Generation"])
async def predictive_sentences(sentence_material: SentenceMaterial) -> Dict[str, str]:
    """
    Generate predictive text and send it to the specified URL.

    Args:
        sentence_material: Object containing text to generate from and response URL

    Returns:
        A dictionary with status information
    """
    try:
        # Generate the text
        generated_text = nlp.predictive_sentences(text=sentence_material.text)

        # Prepare the payload
        payload = json.dumps({
            "text": generated_text,
            "response_type": "in_channel"
        })

        # Send the response
        response = requests.post(
            str(sentence_material.response_url),
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check if the request was successful
        response.raise_for_status()

        return {"status": "Text generated and sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Error sending response: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send response to the provided URL"
        )
    except Exception as e:
        logger.error(f"Error in predictive_sentences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during text generation"
        )
