import base64 as _base64
import zlib as _zlib

from .favicon import content as _favicon
from .styles import content as _styles
from .web_components import content as _web_components


def _decode(content: str) -> bytes:
    z = _base64.b85decode(content)
    return _zlib.decompress(z)


favicon = _decode(_favicon)
"""
Favicon content.

Content-Type: image/x-icon

Example:
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from stopments.embed import favicon

app = FastAPI()

@app.get("/favicon.ico")
async def favicon_ico():
    return HTMLResponse(
        content=favicon,
        headers={"Content-Type": "image/x-icon"},
    )
```
"""

css_content = _decode(_styles)
"""
CSS content from https://unpkg.com/@stoplight/elements/styles.min.css

Content-Type: text/css; charset=utf-8

Example:
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from stopments.embed import css_content

app = FastAPI()

@app.get("/static/styles.min.css")
async def styles_css():
    return HTMLResponse(
        content=css_content,
        headers={"Content-Type": "text/css; charset=utf-8"},
    )
```
"""

js_content = _decode(_web_components)
"""
JavaScript content from https://unpkg.com/@stoplight/elements/web-components.min.js

Content-Type: application/javascript; charset=utf-8

Example:
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from stopments.embed import js_content

app = FastAPI()

@app.get("/static/web-components.min.js")
async def web_components_js():
    return HTMLResponse(
        content=js_content,
        headers={"Content-Type": "application/javascript; charset=utf-8"},
    )
```
"""
