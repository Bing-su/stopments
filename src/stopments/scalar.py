from __future__ import annotations

import json
from enum import Enum

API_REFERENCE = "scalar-api-reference.js"


class SearchHotKey(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"  # noqa: E741
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"  # noqa: E741
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"


class ThemeId(Enum):
    ALTERNATE = "alternate"
    DEFAULT = "default"
    MOON = "moon"
    PURPLE = "purple"
    SOLARIZED = "solarized"
    BLUE_PLANET = "bluePlanet"
    DEEP_SPACE = "deepSpace"
    SATURN = "saturn"
    KEPLER = "kepler"
    ELYSIAJS = "elysiajs"
    FASTIFY = "fastify"
    MARS = "mars"
    LASERWAVE = "laserwave"
    NONE = "none"


class Integration(Enum):
    ADONISJS = "adonisjs"
    DOCUSAURUS = "docusaurus"
    DOTNET = "dotnet"
    ELYSIAJS = "elysiajs"
    EXPRESS = "express"
    FASTAPI = "fastapi"
    FASTIFY = "fastify"
    GO = "go"
    HONO = "hono"
    HTML = "html"
    LARAVEL = "laravel"
    LITESTAR = "litestar"
    NESTJS = "nestjs"
    NEXTJS = "nextjs"
    NITRO = "nitro"
    NUXT = "nuxt"
    PLATFORMATIC = "platformatic"
    REACT = "react"
    RUST = "rust"
    SVELTE = "svelte"
    VUE = "vue"


def dump(key: str, data: object) -> str:
    if not isinstance(data, bool) and not data:
        return ""
    return f"{key}: {json.dumps(data)},"


def get_scalar_html(  # noqa: PLR0913
    *,
    openapi_url: str,
    title: str,
    scalar_js_url: str = "https://cdn.jsdelivr.net/npm/@scalar/api-reference",
    scalar_proxy_url: str = "",
    scalar_favicon_url: str = "https://docs.scalar.com/favicon.svg",
    slug: str | None = None,
    authentication: dict | None = None,
    base_server_url: str = "",
    hide_client_button: bool = False,
    proxy_url: str = "",
    search_hot_key: SearchHotKey = SearchHotKey.K,
    servers: list[dict[str, str]] | None = None,
    show_sidebar: bool = True,
    theme: ThemeId = ThemeId.DEFAULT,
    integration: Integration | None = None,
    persist_auth: bool = False,
) -> str:
    """
    Generates HTML for Scalar API Reference based on OpenAPI specification.

    https://github.com/scalar/scalar/blob/main/packages/types/src/api-reference/api-reference-configuration.ts

    Args:
        openapi_url: URL to an OpenAPI/Swagger document
        title: The title of the OpenAPI document.
        scalar_js_url: URL to Scalar JavaScript library
        scalar_proxy_url: Scalar proxy URL
        scalar_favicon_url: Favicon URL
        slug: The slug of the OpenAPI document used in the URL. If none is passed, the title will be used.
        authentication: Prefill authentication
        base_server_url: Base URL for the API server
        hide_client_button: Whether to hide the client button
        proxy_url: URL to a request proxy for the API client
        search_hot_key: Key used with CTRL/CMD to open the search modal (defaults to 'k' e.g. CMD+k)
        servers: List of OpenAPI server objects
        show_sidebar: Whether to show the sidebar
        theme:  A string to use one of the color presets
        integration: Integration type identifier
        persist_auth: Whether to persist auth to local storage

    Returns:
        HTML document displaying the Scalar API Reference
    """
    servers = servers or []
    authentication = authentication or {}

    return f"""<!doctype html>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    {f'<link rel="shortcut icon" href="{scalar_favicon_url}">' if scalar_favicon_url else ""}
  </head>
  <body>
    <script
      id="api-reference"
      data-url="{openapi_url}"
      {f'data-proxy-url="{scalar_proxy_url}"' if scalar_proxy_url else ""}
    >
    </script>

    <script>
      var configuration = {{
          {dump("slug", slug)}
          {dump("authentication", authentication)}
          {dump("baseServerUrl", base_server_url)}
          {dump("hideClientButton", hide_client_button)}
          {dump("proxyUrl", proxy_url)}
          {dump("searchHotKey", search_hot_key.value)}
          {dump("servers", servers)}
          {dump("showSidebar", show_sidebar)}
          {dump("theme", theme.value)}
          {dump("_integration", integration.value if integration else None)}
          {dump("persistAuth", persist_auth)}
      }}

      document.getElementById('api-reference').dataset.configuration =
        JSON.stringify(configuration)
    </script>

    <script src="{scalar_js_url}"></script>
  </body>
</html>"""
