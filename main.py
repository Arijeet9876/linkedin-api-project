from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

app = FastAPI()

class LinkedInInput(BaseModel):
    linkedin_url: str

@app.post("/extract")
def extract_linkedin_data(input: LinkedInInput):
    url = "https://app.scrapingbee.com/api/v1/"

    params = {
        "api_key": API_KEY,
        "url": input.linkedin_url,
        "render_js": "true",
        "premium_proxy": "true",
        "block_resources": "false",
        "wait": 5000
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail={
                "error_status_code": response.status_code,
                "error_response": response.text
            }
        )

    soup = BeautifulSoup(response.text, "lxml")

    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else "Name not found"

    headline_tag = soup.find("div", {"class": "text-body-medium break-words"})
    headline = headline_tag.get_text(strip=True) if headline_tag else "Headline not found"

    return {
        "status": "success",
        "name": name,
        "headline": headline,
        "raw_html_snippet": response.text[:500]
    }
