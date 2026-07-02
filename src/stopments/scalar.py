from __future__ import annotations

import json
from enum import Enum
from typing import Any

from .conv import to_camel

API_REFERENCE = "scalar-api-reference.js"


class Layout(Enum):
    MODERN = "modern"
    CLASSIC = "classic"


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


class Theme(Enum):
    ALTERNATE = "alternate"
    DEFAULT = "default"
    MOON = "moon"
    PURPLE = "purple"
    SOLARIZED = "solarized"
    BLUE_PLANET = "bluePlanet"
    SATURN = "saturn"
    KEPLER = "kepler"
    MARS = "mars"
    DEEP_SPACE = "deepSpace"
    LASERWAVE = "laserwave"
    NONE = "none"


class DocumentDownloadType(Enum):
    JSON = "json"
    YAML = "yaml"
    BOTH = "both"
    DIRECT = "direct"
    NONE = "none"


class OperationTitleSource(Enum):
    SUMMARY = "summary"
    PATH = "path"


class OrderSchemaPropertiesBy(Enum):
    ALPHA = "alpha"
    PRESERVE = "preserve"


class ShowDeveloperTools(Enum):
    ALWAYS = "always"
    LOCALHOST = "localhost"
    NEVER = "never"


class ForceDarkModeState(Enum):
    DARK = "dark"
    LIGHT = "light"


_HTML_KEYS = {"title", "scalar_js_url", "overrides"}


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def get_scalar_html(  # noqa: PLR0913
    *,
    title: str | None = None,
    scalar_js_url: str = "https://cdn.jsdelivr.net/npm/@scalar/api-reference",
    url: str | None = None,
    favicon: str | None = None,
    content: str | dict[str, Any] | None = None,
    sources: list[dict[str, Any]] | None = None,
    layout: Layout | None = None,
    theme: Theme | None = None,
    show_sidebar: bool | None = None,
    hide_search: bool | None = None,
    hide_models: bool | None = None,
    hide_client_button: bool | None = None,
    hide_test_request_button: bool | None = None,
    hide_dark_mode_toggle: bool | None = None,
    dark_mode: bool | None = None,
    force_dark_mode_state: ForceDarkModeState | None = None,
    document_download_type: DocumentDownloadType | None = None,
    default_open_first_tag: bool | None = None,
    default_open_all_tags: bool | None = None,
    expand_all_model_sections: bool | None = None,
    expand_all_responses: bool | None = None,
    expand_all_schema_properties: bool | None = None,
    order_required_properties_first: bool | None = None,
    order_schema_properties_by: OrderSchemaPropertiesBy | None = None,
    operation_title_source: OperationTitleSource | None = None,
    show_operation_id: bool | None = None,
    models_section_label: str | None = None,
    proxy_url: str | None = None,
    authentication: dict[str, Any] | None = None,
    persist_auth: bool | None = None,
    servers: list[dict[str, Any]] | None = None,
    oauth2_redirect_uri: str | None = None,
    default_http_client: dict[str, Any] | None = None,
    meta_data: dict[str, Any] | None = None,
    localization: dict[str, Any] | None = None,
    path_routing: dict[str, Any] | None = None,
    mcp: dict[str, Any] | None = None,
    agent: dict[str, Any] | None = None,
    custom_css: str | None = None,
    hidden_clients: bool | list[str] | dict[str, Any] | None = None,
    search_hot_key: SearchHotKey | None = None,
    show_developer_tools: ShowDeveloperTools | None = None,
    telemetry: bool | None = None,
    with_default_fonts: bool | None = None,
    overrides: dict[str, Any] | None = None,
) -> str:
    """
    Generate an HTML document that embeds the Scalar API Reference.

    Configuration follows https://scalar.com/products/api-references/configuration
    with Python snake_case argument names.
    """
    config = {
        to_camel(key): _jsonable(value)
        for key, value in locals().items()
        if key not in _HTML_KEYS and value is not None
    }

    if overrides:
        config.update(_jsonable(overrides))

    return f"""<!doctype html>
<html>
  <head>
    <title>{title or "Scalar"}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
  </head>
  <body>
    <div id="app"></div>
    <script src="{scalar_js_url}"></script>
    <script>
      Scalar.createApiReference("#app", {json.dumps(config)})
    </script>
  </body>
</html>"""
