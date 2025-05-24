# Stopments

Stoplight elements static files

Refered from FastAPI's #5168 PR

It includes the following files:

- `styles.min.css`
- `web-components.min.js`
- `favicon.ico`
- `scalar-api-reference.js` (for [scalar](https://scalar.com/))

The static files were collected on the same date as this package version.

## Installation

```bash
pip install stopments
```

## Usage

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from stopments import get_stoplight_elements_html

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs/", include_in_schema=False)
async def docs():
    html = get_stoplight_elements_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title="API Documentation",
    )
    return HTMLResponse(content=html)
```

or you can use embedded static files

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from stopments import get_stoplight_elements_html

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(packages=[("stopments", "static")]))

@app.get("/docs/", include_in_schema=False)
async def docs():
    html = get_stoplight_elements_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title="API Documentation",
        stoplight_elements_css_url="/static/styles.min.css",
        stoplight_elements_js_url="/static/web-components.min.js",
        stoplight_elements_favicon_url="/static/favicon.ico",
    )
    return HTMLResponse(content=html)
```

## References

- [FastAPI PR #5168](https://github.com/fastapi/fastapi/pull/5168)
- [Stoplight Elements Docs - Usage with HTML](https://docs.stoplight.io/docs/elements/a71d7fcfefcd6-elements-in-html)
