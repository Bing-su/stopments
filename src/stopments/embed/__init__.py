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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    return HTMLResponse(content=favicon, media_type="image/x-icon")
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

@app.get("/static/styles.min.css", include_in_schema=False)
async def styles_css():
    return HTMLResponse(content=css_content, media_type="text/css; charset=utf-8")
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

@app.get("/static/web-components.min.js", include_in_schema=False)
async def web_components_js():
    return HTMLResponse(
        content=js_content, media_type="application/javascript; charset=utf-8"
    )
```
"""

del _base64, _zlib, _favicon, _styles, _web_components
