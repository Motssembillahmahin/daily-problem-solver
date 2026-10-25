# URL Shortener

A simple URL shortener API built with FastAPI.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## API Endpoints

- `POST /shorten` - Shorten a URL
- `GET /{code}` - Redirect to original URL
- `GET /stats/{code}` - Get URL statistics
