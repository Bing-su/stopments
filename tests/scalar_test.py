import json
import re

from stopments.scalar import (
    DocumentDownloadType,
    ForceDarkModeState,
    Layout,
    OperationTitleSource,
    OrderSchemaPropertiesBy,
    SearchHotKey,
    ShowDeveloperTools,
    Theme,
    get_scalar_html,
)


def config_from(html: str) -> dict:
    match = re.search(r'Scalar\.createApiReference\("#app", (.*?)\)', html)
    assert match
    return json.loads(match.group(1))


def test_scalar_uses_current_initialization():
    html = get_scalar_html(url="/openapi.json")
    assert 'Scalar.createApiReference("#app"' in html
    assert "data-configuration" not in html
    assert "data-url" not in html


def test_scalar_passes_document_inputs():
    assert config_from(get_scalar_html(url="/openapi.json")) == {"url": "/openapi.json"}
    assert config_from(get_scalar_html(content={"openapi": "3.1.0"})) == {
        "content": {"openapi": "3.1.0"}
    }
    assert config_from(get_scalar_html(sources=[{"url": "/a.json"}])) == {
        "sources": [{"url": "/a.json"}]
    }


def test_scalar_maps_snake_case_to_scalar_keys():
    config = config_from(
        get_scalar_html(
            url="/openapi.json",
            custom_css="body{}",
            default_http_client={"targetKey": "python", "clientKey": "requests"},
            default_open_first_tag=False,
            default_open_all_tags=True,
            expand_all_schema_properties=True,
            force_dark_mode_state=ForceDarkModeState.DARK,
            hide_test_request_button=True,
            meta_data={"title": "Docs"},
            models_section_label="Schemas",
            oauth2_redirect_uri="/oauth",
            order_schema_properties_by=OrderSchemaPropertiesBy.PRESERVE,
            path_routing={"basePath": "/docs"},
            show_operation_id=True,
            favicon="/favicon.svg",
        )
    )
    assert config["customCss"] == "body{}"
    assert config["defaultHttpClient"] == {
        "targetKey": "python",
        "clientKey": "requests",
    }
    assert config["defaultOpenFirstTag"] is False
    assert config["defaultOpenAllTags"] is True
    assert config["expandAllSchemaProperties"] is True
    assert config["forceDarkModeState"] == "dark"
    assert config["hideTestRequestButton"] is True
    assert config["metaData"] == {"title": "Docs"}
    assert config["modelsSectionLabel"] == "Schemas"
    assert config["oauth2RedirectUri"] == "/oauth"
    assert config["orderSchemaPropertiesBy"] == "preserve"
    assert config["pathRouting"] == {"basePath": "/docs"}
    assert config["showOperationId"] is True
    assert config["favicon"] == "/favicon.svg"


def test_scalar_keeps_explicit_false_and_empty_values():
    config = config_from(
        get_scalar_html(
            show_sidebar=False,
            hidden_clients=[],
            authentication={},
            servers=[],
            telemetry=False,
        )
    )
    assert config == {
        "authentication": {},
        "hiddenClients": [],
        "servers": [],
        "showSidebar": False,
        "telemetry": False,
    }


def test_scalar_serializes_enums():
    config = config_from(
        get_scalar_html(
            layout=Layout.CLASSIC,
            theme=Theme.MOON,
            document_download_type=DocumentDownloadType.DIRECT,
            operation_title_source=OperationTitleSource.PATH,
            search_hot_key=SearchHotKey.L,
            show_developer_tools=ShowDeveloperTools.NEVER,
        )
    )
    assert config == {
        "documentDownloadType": "direct",
        "layout": "classic",
        "operationTitleSource": "path",
        "searchHotKey": "l",
        "showDeveloperTools": "never",
        "theme": "moon",
    }


def test_scalar_overrides_win_last():
    config = config_from(
        get_scalar_html(
            url="/openapi.json",
            theme=Theme.DEFAULT,
            overrides={"theme": "purple", "x-test": {"hotKey": SearchHotKey.A}},
        )
    )
    assert config["url"] == "/openapi.json"
    assert config["theme"] == "purple"
    assert config["x-test"] == {"hotKey": "a"}
