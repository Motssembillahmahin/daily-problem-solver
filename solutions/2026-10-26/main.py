#!/usr/bin/env python3
"""
URL Shortener - Simple in-memory URL shortener
Usage: python main.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import string
import random

app = FastAPI(title="URL Shortener")

# In-memory storage
url_database = {}

class URLRequest(BaseModel):
    url: str
    custom_code: str = None

def generate_short_code(url: str) -> str:
    """Generate a short code from URL hash."""
    hash_obj = hashlib.md5(url.encode())
    return hash_obj.hexdigest()[:6]

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    """Shorten a URL."""
    # Use custom code or generate one
    if request.custom_code:
        code = request.custom_code
    else:
        code = generate_short_code(request.url)
    
    # Store mapping
    url_database[code] = request.url
    
    return {
        "original": request.url,
        "shortened": f"http://localhost:8000/{code}",
        "code": code
    }

@app.get("/{code}")
async def redirect_to_url(code: str):
    """Redirect to original URL."""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=url_database[code])

@app.get("/stats/{code}")
async def get_stats(code: str):
    """Get URL statistics."""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {
        "code": code,
        "original": url_database[code],
        "access_count": url_database.get(f"{code}_count", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
