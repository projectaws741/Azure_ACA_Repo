import os
from typing import Any, Dict

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Frontend App")

# Read backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    # Optional: you can still run locally with a default
    BACKEND_URL = "http://localhost:3500"


def build_html_page(title: str, body_html: str) -> str:
    """Simple HTML wrapper so we don't need templates folder."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                color: #333;
            }}
            .grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
            }}
            .card {{
                border: 1px solid #ccc;
                padding: 12px;
                border-radius: 8px;
                max-width: 220px;
            }}
            img {{
                max-width: 100%;
                border-radius: 4px;
            }}
            .doc-list li {{
                margin-bottom: 6px;
            }}
            a {{
                text-decoration: none;
                color: #0078d4;
            }}
        </style>
    </head>
    <body>
        {body_html}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
    <h1>Frontend App</h1>
    <p>This frontend talks to a backend using the BACKEND_URL environment variable.</p>
    <ul>
        <li><a href="/albums">View Albums</a></li>
        <li><a href="/work">View Work Documents</a></li>
    </ul>
    <p>Current BACKEND_URL: <code>{backend_url}</code></p>
    """.format(backend_url=BACKEND_URL)
    return build_html_page("Frontend Home", html)


@app.get("/albums", response_class=HTMLResponse)
async def show_albums():
    """Calls backend /albums and shows images."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{BACKEND_URL}/albums")
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error calling backend /albums: {e}")

    data: Dict[str, Any] = resp.json()
    items = data.get("items", [])

    cards = []
    for item in items:
        title = item.get("title", "Untitled")
        url = item.get("url", "#")
        cards.append(f"""
            <div class="card">
                <h3>{title}</h3>
                <img src="{url}" alt="{title}" />
            </div>
        """)

    body = f"""
    <h1>Albums (from Backend)</h1>
    <p>Fetched from: <code>{BACKEND_URL}/albums</code></p>
    <div class="grid">
        {''.join(cards)}
    </div>
    <p><a href="/">Back to Home</a></p>
    """
    return build_html_page("Albums", body)


@app.get("/work", response_class=HTMLResponse)
async def show_work_docs():
    """Calls backend /work and shows a document list."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{BACKEND_URL}/work")
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error calling backend /work: {e}")

    data: Dict[str, Any] = resp.json()
    items = data.get("items", [])

    list_items = []
    for item in items:
        name = item.get("name", "Unnamed.doc")
        desc = item.get("description", "")
        list_items.append(f"<li><strong>{name}</strong> – {desc}</li>")

    body = f"""
    <h1>Work Documents (from Backend)</h1>
    <p>Fetched from: <code>{BACKEND_URL}/work</code></p>
    <ul class="doc-list">
        {''.join(list_items)}
    </ul>
    <p><a href="/">Back to Home</a></p>
    """
    return build_html_page("Work Documents", body)
