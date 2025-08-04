from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PROXYCURL_API_KEY")

app = FastAPI()

class LinkedInInput(BaseModel):
    linkedin_url: str

@app.post("/extract")
def extract_linkedin_data(input: LinkedInInput):
    url = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"url": input.linkedin_url}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch data from LinkedIn")

    return response.json()
