import pytest
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient

from stopments import get_stoplight_elements_html
from stopments.embed import css_content, favicon, js_content


def fastapi_app():
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}

    @app.get("/docs")
    async def docs():
        html = get_stoplight_elements_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation",
        )
        return HTMLResponse(content=html)

    return app


def fastapi_app_embed():
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.get("/static/web-components.min.js")
    async def web_components_js():
        return HTMLResponse(
            content=js_content,
            headers={"Content-Type": "application/javascript; charset=utf-8"},
        )

    @app.get("/static/styles.min.css")
    async def styles_css():
        return HTMLResponse(
            content=css_content,
            headers={"Content-Type": "text/css; charset=utf-8"},
        )

    @app.get("/favicon.ico")
    async def favicon_ico():
        return HTMLResponse(
            content=favicon,
            headers={"Content-Type": "image/x-icon"},
        )

    @app.get("/")
    async def index():
        return {"message": "Hello, World!"}

    @app.get("/docs")
    async def docs():
        html = get_stoplight_elements_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title="API Documentation",
            stoplight_elements_css_url="/static/styles.min.css",
            stoplight_elements_js_url="/static/web-components.min.js",
            stoplight_elements_favicon_url="/favicon.ico",
        )
        return HTMLResponse(content=html)

    return app


@pytest.mark.parametrize("app", [fastapi_app(), fastapi_app_embed()])
def test_fastapi(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    response = client.get("/docs")
    assert response.status_code == 200
    assert "API Documentation" in response.text
