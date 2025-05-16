import pytest
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

from stopments import get_stoplight_elements_html
from stopments.embed import (
    css_content,
    favicon_content,
    js_content,
    scalar_api_reference_js_content,
)
from stopments.scalar import get_scalar_html


def fastapi_app():
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}

    @app.get("/docs", include_in_schema=False)
    async def docs():
        html = get_stoplight_elements_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation",
        )
        return HTMLResponse(content=html)

    @app.get("/scalar", include_in_schema=False)
    async def scalar():
        html = get_scalar_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation Scalar",
        )
        return HTMLResponse(content=html)

    return app


def fastapi_app_embed():
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/static/web-components.min.js", include_in_schema=False)
    async def web_components_js():
        return HTMLResponse(
            content=js_content,
            media_type="application/javascript; charset=utf-8",
        )

    @app.get("/static/styles.min.css", include_in_schema=False)
    async def styles_css():
        return HTMLResponse(
            content=css_content,
            media_type="text/css; charset=utf-8",
        )

    @app.get("/static/favicon.ico", include_in_schema=False)
    async def favicon_ico():
        return HTMLResponse(
            content=favicon_content,
            media_type="image/x-icon",
        )

    @app.get("/static/scalar-api-reference.js", include_in_schema=False)
    async def scalar_api_reference_js():
        return HTMLResponse(
            content=scalar_api_reference_js_content,
            media_type="application/javascript; charset=utf-8",
        )

    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}

    @app.get("/docs", include_in_schema=False)
    async def docs():
        html = get_stoplight_elements_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation",
            stoplight_elements_css_url="/static/styles.min.css",
            stoplight_elements_js_url="/static/web-components.min.js",
            stoplight_elements_favicon_url="/static/favicon.ico",
        )
        return HTMLResponse(content=html)

    @app.get("/scalar", include_in_schema=False)
    async def scalar():
        html = get_scalar_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation Scalar",
            scalar_js_url="/static/scalar-api-reference.js",
            scalar_favicon_url="/static/favicon.ico",
        )
        return HTMLResponse(content=html)

    return app


def fastapi_app_embed_gzip():
    app = fastapi_app_embed()
    app.add_middleware(GZipMiddleware, minimum_size=100)
    return app


def fastapi_app_staticfiles():
    app = FastAPI(docs_url=None, redoc_url=None)

    app.mount("/static", StaticFiles(packages=[("stopments", "static")]))

    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}

    @app.get("/docs", include_in_schema=False)
    async def docs():
        html = get_stoplight_elements_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation",
            stoplight_elements_css_url="/static/styles.min.css",
            stoplight_elements_js_url="/static/web-components.min.js",
            stoplight_elements_favicon_url="/static/favicon.ico",
        )
        return HTMLResponse(content=html)

    @app.get("/scalar", include_in_schema=False)
    async def scalar():
        html = get_scalar_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation Scalar",
            scalar_js_url="/static/scalar-api-reference.js",
            scalar_favicon_url="/static/favicon.ico",
        )
        return HTMLResponse(content=html)

    return app


def test_fastapi():
    app = fastapi_app()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    response = client.get("/docs")
    assert response.status_code == 200
    assert "API Documentation" in response.text
    assert "web-components.min.js" in response.text
    assert "styles.min.css" in response.text
    assert "favicon.ico" in response.text

    response = client.get("/scalar")
    assert response.status_code == 200
    assert "API Documentation" in response.text
    assert "api-reference" in response.text
    assert "favicon.ico" in response.text or "favicon.svg" in response.text


@pytest.mark.parametrize(
    "app",
    [
        fastapi_app_embed(),
        fastapi_app_embed_gzip(),
        fastapi_app_staticfiles(),
    ],
)
def test_fastapi_embed(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    response = client.get("/docs")
    assert response.status_code == 200
    assert "API Documentation" in response.text

    response = client.get("/static/web-components.min.js")
    assert response.status_code == 200

    response = client.get("/static/styles.min.css")
    assert response.status_code == 200

    response = client.get("/static/favicon.ico")
    assert response.status_code == 200

    response = client.get("/static/scalar-api-reference.js")
    assert response.status_code == 200
