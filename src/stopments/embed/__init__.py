from importlib.resources import files as _files
from typing import Final

_MODULE = "stopments.static"

favicon_content: Final[bytes] = _files(_MODULE).joinpath("favicon.ico").read_bytes()
"""
Favicon content from https://docs.stoplight.io/favicons/favicon.ico

Content-Type: image/x-icon

Example
-------

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from stopments.embed import favicon_content

app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    return HTMLResponse(content=favicon_content, media_type="image/x-icon")
```
"""


css_content: Final[bytes] = _files(_MODULE).joinpath("styles.min.css").read_bytes()
"""
CSS content from https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css

Content-Type: text/css; charset=utf-8

Example
-------

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

js_content: Final[bytes] = (
    _files(_MODULE).joinpath("web-components.min.js").read_bytes()
)
"""
JavaScript content from https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js

Content-Type: application/javascript; charset=utf-8

Example
-------

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

scalar_api_reference_js_content: Final[bytes] = (
    _files(_MODULE).joinpath("scalar-api-reference.js").read_bytes()
)
"""
JavaScript content from https://cdn.jsdelivr.net/npm/@scalar/api-reference
Content-Type: application/javascript; charset=utf-8

Example
-------

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from stopments.embed import scalar_api_reference_js_content

app = FastAPI()

@app.get("/static/scalar-api-reference.js", include_in_schema=False)
async def scalar_api_reference_js():
    return HTMLResponse(
        content=scalar_api_reference_js_content, media_type="application/javascript; charset=utf-8"
    )
```
"""

del _files, _MODULE

__all__ = [
    "css_content",
    "favicon_content",
    "js_content",
    "scalar_api_reference_js_content",
]
